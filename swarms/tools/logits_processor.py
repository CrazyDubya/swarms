import torch
try:
    from transformers import (
        LogitsWarper,
        PreTrainedTokenizer,
        StoppingCriteria,
    )
except ImportError:
    # Handle newer transformers versions
    from transformers import PreTrainedTokenizer
    try:
        from transformers import StoppingCriteria
    except ImportError:
        # Create a dummy StoppingCriteria for newer versions
        class StoppingCriteria:
            """
            A dummy implementation of the StoppingCriteria class.

            This class is provided as a compatibility fallback for newer versions
            of the transformers library where the StoppingCriteria class might not
            be available. It always returns False, indicating that the stopping
            criteria are never met.
            """
            def __call__(self, input_ids, scores, **kwargs):
                return False
    
    try:
        from transformers import LogitsWarper
    except ImportError:
        # Create a dummy LogitsWarper for newer versions
        class LogitsWarper:
            """
            A fallback implementation of the LogitsWarper class for compatibility
            with newer versions of the transformers library where LogitsWarper
            might not be available.

            This dummy implementation simply returns the scores unchanged.
            """
            def __call__(self, input_ids, scores):
                return scores


class StringStoppingCriteria(StoppingCriteria):
    def __init__(self, tokenizer: PreTrainedTokenizer, prompt_length: int):
        self.tokenizer = tokenizer
        self.prompt_length = prompt_length

    def __call__(
        self,
        input_ids: torch.LongTensor,
        _,
    ) -> bool:
        if len(input_ids[0]) <= self.prompt_length:
            return False

        last_token_id = input_ids[0][-1]
        last_token = self.tokenizer.decode(
            last_token_id, skip_special_tokens=True
        )

        result = '"' in last_token

        return result


class NumberStoppingCriteria(StoppingCriteria):
    def __init__(
        self,
        tokenizer: PreTrainedTokenizer,
        prompt_length: int,
        precision: int = 3,
    ):
        self.tokenizer = tokenizer
        self.precision = precision
        self.prompt_length = prompt_length

    def __call__(
        self,
        input_ids: torch.LongTensor,
        scores: torch.FloatTensor,
    ) -> bool:
        decoded = self.tokenizer.decode(
            input_ids[0][self.prompt_length :],
            skip_special_tokens=True,
        )

        if decoded.count(".") > 1:
            return True

        if (
            decoded.count(".") == 1
            and len(decoded.strip().split(".")[1]) > self.precision
        ):
            return True

        if (
            len(decoded) > 1
            and any(c.isdigit() for c in decoded)
            and decoded[-1] in [" ", "\n"]
        ):
            return True

        return False


class OutputNumbersTokens(LogitsWarper):
    def __init__(self, tokenizer: PreTrainedTokenizer, prompt: str):
        self.tokenizer = tokenizer
        self.tokenized_prompt = tokenizer(prompt, return_tensors="pt")
        vocab_size = len(tokenizer)
        self.allowed_mask = torch.zeros(vocab_size, dtype=torch.bool)

        for _, token_id in tokenizer.get_vocab().items():
            token_str = tokenizer.decode(token_id).strip()

            if token_str == "" or (
                all(c.isdigit() or c == "." for c in token_str)
                and token_str.count(".") <= 1
            ):
                self.allowed_mask[token_id] = True

    def __call__(self, _, scores):
        mask = self.allowed_mask.expand_as(scores)
        scores[~mask] = -float("inf")

        return scores
