import torch


import numpy as np
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer


class BertClassifier():

    def __init__(self,
                 model_path: str = "cointegrated/rubert-tiny",
                 max_length: int = 32,
                 padding: str = "max_length") -> None:

        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            num_labels=2,
            output_attentions=False,
            output_hidden_states=False)
        self.max_length = max_length
        self.padding = padding

    def predict(self, text: str, device: str = "cpu"):

        ids, mask = self._encode(text)
        ids, mask = ids.to(device), mask.to(device)
        with torch.no_grad():
            output = self.model(ids, token_type_ids=None, attention_mask=mask)
        prediction = np.argmax(output.logits.cpu().numpy()).flatten().item()
        return prediction

    def predict_proba(self, text: str, device: str = "cpu"):
        ids, mask = self._encode(text)
        ids, mask = ids.to(device), mask.to(device)
        with torch.no_grad():
            output = self.model(ids, token_type_ids=None, attention_mask=mask)
        prediction = output.logits.cpu().numpy()[:, 1].item()
        return prediction

    def _encode(self, text):
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
