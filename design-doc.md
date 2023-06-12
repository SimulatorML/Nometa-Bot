# Problem Statement and Project Objectives

The problem of meta-questions in large chats, where both novice and experienced specialists communicate, is common. In personal meetings, people try to be polite and not immediately jump to the problem, but chatting is different. Instead of showing politeness, users have to wait for someone to formulate their question. This leads to a loss of productivity and dissatisfaction among participants.

By reducing the number of meta-questions in chats, we can make conversations more productive and enjoyable for everyone involved. Additionally, by encouraging people to be more mindful about the questions they ask, we can help them become better communicators overall. This can lead to more effective collaboration, better relationships, and increased success in various areas of life.

Overall, the goal of this project is to promote more thoughtful and intentional communication in all types of interactions, whether they be in personal or professional contexts, or just for fun :).

---

# Metrics and Losses

### Online Metrics

- *Number of false positives*: This metric measures the number of times that the *****Nometa-Bot***** responds to a question that is not actually a meta-question. False positives are undesirable because they can annoy users and reduce the bot's effectiveness.
- *Number of missed meta-questions*: This metric measures the number of times that the Nometa-Bot fails to respond to a meta-question. Missed meta-questions are also undesirable because they indicate the questions that our bot is not able to detect. While users may not necessarily be frustrated by missed meta-questions, they can reduce the bot's effectiveness in improving communication and productivity in the chat.

By tracking these metrics over time, we can evaluate the overall effectiveness of the Nometa-Bot and make improvements to its algorithm to optimize its performance based on the specific requirements of the project.

---

### Offline Metrics

The second set of metrics are offline metrics, which measure the performance of the Nometa-Bot after the fact, based on data that has been collected from previous interactions. Since there is a strong class imbalance in meta-questions, and we want to minimize missed meta-questions

- *Recall@specificity > N%*: This metric measures how well the Nometa-Bot is able to correctly identify meta-questions (i.e. high recall) while minimizing false positives (i.e. high specificity). The value of N% will be determined based on the specific requirements of the project.
- *Recall@precision > N%*: This metric measures how well the Nometa-Bot is able to correctly identify meta-questions (i.e. high recall) while minimizing false positives (i.e. high precision). The value of N% will be determined based on the specific requirements of the project.

By tracking these metrics over time, we can evaluate the overall effectiveness of the Nometa-Bot and make improvements to its algorithm to optimize its performance based on the specific requirements of the project.

---

### Technical

- *Response time*: This metric measures how quickly the Nometa-Bot is able to respond to a meta-question after it has been asked in a chat. A fast response time is desirable because it reduces wait times for users and improves their overall experience.
- *RAM consumption*: This metric measures how much memory the Nometa-Bot uses while it is running. Optimizing RAM consumption is important because it can help to reduce costs associated with hosting the bot and improve its scalability.
- *Disk-memory consumption*: This metric measures how much disk space the Nometa-Bot uses to store data. Optimizing disk-memory consumption is important because it can help to reduce costs associated with hosting the bot and improve its scalability.

By tracking these technical metrics over time, we can identify opportunities to optimize the performance of the Nometa-Bot and ensure that it is running efficiently.

---

### Losses

- *LogLoss*: This loss measures the difference between the predicted probability of a meta-question and the actual label. A low LogLoss is desirable because it indicates that the Nometa-Bot is accurately classifying meta-questions.

By tracking this loss over time, we can evaluate the effectiveness of the Nometa-Bot's algorithm and make improvements to optimize its performance.

---

# Data Collection

The data for training model (meta and non-meta questions) is obtained by parsing various Telegram chats using a custom-built parser. During the parsing process, all messages are cleaned of unnecessary symbols and characters. Any questions that have a link to the website nometa.xyz in their responses are labeled as 1 (positive), while all other questions are labeled as 0 (negative).

---

# Data Annotation

The data will be annotated using a combination of human annotation and ChatGPT. Questions will be presented to ChatGPT with special instructions and additional information, and based on this information, the appropriate class will be assigned to the question. Human annotators will also review and correct any errors made by the model to ensure accuracy.

---

# Data Storage

The data will be stored in .csv format tables, with version control managed using cloud storage and DVC (Data Version Control). This will allow for easy access and sharing of the data among team members and provide a record of changes made to the data over time.

---

# Validation

---

Validation is an important step in model development to ensure that the model performs well on new, unseen data. In our design, we will implement a validation scheme where the dataset will be divided into two parts - a training set and a test set. The test set will be held out during training and only used for evaluating the model's performance. We will calculate evaluation metrics, described above, on the test set to gauge the model's performance on new data. These metrics will guide us in making decisions about model selection and parameter tuning, and help ensure that our model is robust and performs well in real-world scenarios.

# Baseline Model

As part of our project design, we have selected three models to serve as the baseline for our Nometa-Bot: TF-IDF n-grams with Logistic Regression, ruBERT embeddings with Logistic Regression, and fine-tuned ruBERT. These models were chosen after careful consideration and research as they represent a range of complexity and performance and have been shown to perform well in natural language processing tasks.

- *TF-IDF n-grams with Logistic Regression*, is a simple and effective model that represents text as a bag-of-words and uses logistic regression to classify the text based on frequency of occurrence of tokens. This model will serve as a good starting point in our project as it is straightforward and easy to implement.
- *RuBERT embeddings with Logistic Regression*, is more complex and uses pre-trained contextual embeddings to capture the meaning and context of words. This will allow our bot to better understand the intent behind the meta-questions and improve its accuracy in identifying them.
- *Fine-tuned ruBERT* model is a state-of-the-art model that has shown excellent performance in various natural language processing tasks. We will fine-tune this model on our specific task of identifying meta-questions to further improve the accuracy of our bot.

Overall, these three models will serve as our baseline in developing the Nometa-Bot and will be evaluated to determine the best model for our specific task of identifying meta-questions in a chat.

---

# Error Analysis

WIP

---

# Training Pipeline

The training pipeline for our  baseline models. The first model combines Logistic Regression with TF-IDF ngrams, while the second model employs Fine-Tuned BERT.

For the Logistic Regression + TF-IDF ngrams model, the pipeline includes data extraction, symbol removal, TF-IDF ngrams calculation, logistic regression classification, and validation on a holdout dataset.

![Screenshot from 2023-05-19 11-40-06.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/82afcf7e-52e1-45e7-8b4f-76d1600b829a/Screenshot_from_2023-05-19_11-40-06.png)

In the case of the Fine-Tuned BERT model, the pipeline consists of loading the pre-trained model, data loading, text transformation using a pre-trained tokenizer, training the classifier layer on the BERT model, and validation on a holdout dataset.

![Screenshot from 2023-05-19 11-44-39.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/de8feaf7-5ba3-4d9f-a015-9d93db2a34f2/Screenshot_from_2023-05-19_11-44-39.png)

Throughout the training process, we will collect metrics and monitor loss curves to evaluate the models' performance. These metrics and loss curves will provide insights into the models' convergence and classification accuracy.

---

# Inference Pipeline

The Inference Pipeline loads a pre-trained model upon service startup and preprocesses each item accordingly before making predictions. The data undergoes model-specific preprocessing, and the processed data is then passed through the loaded model for prediction generation. This pipeline ensures consistent and accurate predictions by aligning the data with the model's requirements. It allows for efficient model deployment and maintenance within the service architecture.

![Screenshot from 2023-05-19 12-22-06.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b55bae58-cb6e-496d-9efa-096779440ac6/Screenshot_from_2023-05-19_12-22-06.png)

---

# Integration and Deployment

After training and debugging the model, it will be integrated into a Telegram bot and deployed on a server. Integration testing and configuration will be conducted, and scaling methods will be identified to ensure stable bot operation as the load increases.

In the end, the developed Telegram bot will be able to automatically respond to meta-questions in the chat, which will help reduce the number of meta-questions and improve chat efficiency.
