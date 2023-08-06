from typing import Tuple, List
import torch


from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer


class BertClassifier():
    """
    A classifier based on BERT (Bidirectional Encoder Representations from
    Transformers) model. It uses a pre-trained BERT model for sequence
    classification and fine-tunes it on a specific task. The class provides
    methods for making predictions and computing probabilities.

    Args:
        model_path (str): Path to the pre-trained BERT model.
        max_length (int): Maximum sequence length for input text. Default is 32.
        padding (str): Padding strategy for the input text. Default is
        "max_length" device (str): Device to run the model on. Default is "cpu".

    Attributes:
        tokenizer: BERT tokenizer for encoding input text.
        model: Fine-tuned BERT model for sequence classification.
        max_length (int): Maximum sequence length for input text.
        padding (str): Padding strategy for the input text.
        device (str): Device to run the model on.
    """

    def __init__(self,
                 model_path: str = "cointegrated/rubert-tiny",
                 max_length: int = 32,
                 padding: str = "max_length",
                 device: str = "cpu",
                 threshold: float = 0.9) -> None:
        """
        Initializes the BertClassifier.

        Args:
            model_path (str): Path to the pre-trained BERT model.
            max_length (int): Maximum sequence length for input text.
            Default is 32.
            padding (str): Padding strategy for the input text.
            Default is "max_length".
            device (str): Device to run the model on. Default is "cpu".
        """

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            num_labels=2,
            output_attentions=False,
            output_hidden_states=False)
        self.max_length = max_length
        self.padding = padding
        self.device = device
        self.threshold = threshold

    def predict(self, text: str) -> int:
        """
        Makes a prediction for the given input text.

        Args:
            text (str): Input text for classification.

        Returns:
            int: Predicted class label (0 or 1).
        """

        ids, mask = self._encode(text)
        ids, mask = ids.to(self.device), mask.to(self.device)
        with torch.no_grad():
            output = self.model(ids, token_type_ids=None, attention_mask=mask)
        prediction = (output.logits.cpu().numpy())[:, 1].item()
        if prediction >= self.threshold:

            prediction = 1
        else:
            prediction = 0
        return prediction

    def predict_proba(self, text: str) -> float:
        """
        Computes the probability of the positive class for the given input text.

        Args:
            text (str): Input text for classification.

        Returns:
            float: Probability of the positive class.
        """

        ids, mask = self._encode(text)
        ids, mask = ids.to(self.device), mask.to(self.device)
        with torch.no_grad():
            output = self.model(ids, token_type_ids=None, attention_mask=mask)
        prediction = output.logits.cpu().numpy()[:, 1].item()
        return prediction

    def _encode(self, text) -> Tuple[List[int], List[int]]:
        """
        Encodes the text using the tokenizer and returns the encoded input and
        attention mask.

        Args:
            text (str): The input text to encode.

        Returns:
            torch.Tensor, torch.Tensor: The encoded input and attention mask as
            PyTorch tensors.
        """
        ids = []
        attention_mask = []
        encoding = self.tokenizer.encode_plus(
            text,
            max_length=self.max_length,
            padding=self.padding,
            add_special_tokens=True,
            return_attention_mask=True,
            return_tensors='pt')

        ids.append(encoding['input_ids'])
        attention_mask.append(encoding['attention_mask'])
        ids = torch.cat(ids)
        attention_mask = torch.cat(attention_mask)
        return ids, attention_mask
