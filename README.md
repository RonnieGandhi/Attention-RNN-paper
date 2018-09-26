# Attention-based-biderictional-LSTM-Network-for-Relation-Classification
Implementing paper

# DATA
1. GoogleNews-vectors-negative300.bin : use of Google's trained word2vec model in Python
    !it  can be found from : http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/
    
2. SemEval2010_task8_all_data : data we'll use for training and evaluation 
    !it can be foun from : https://docs.google.com/leaf?id=0B_jQiLugGTAkMDQ5ZjZiMTUtMzQ1Yy00YWNmLWJlZDYtOWY1ZDMwY2U4YjFk&sort=name&layout=list&num=50
    
    ### Distribution for Dataset
* **SemEval-2010 Task #8 Dataset [[Download](https://drive.google.com/file/d/0B_jQiLugGTAkMDQ5ZjZiMTUtMzQ1Yy00YWNmLWJlZDYtOWY1ZDMwY2U4YjFk/view?layout=list&ddrp=1&sort=name&num=50#)]**

| Relation           | Train Data          | Test Data           | Total Data           |
|--------------------|:-------------------:|:-------------------:|:--------------------:|
| Cause-Effect       | 1,003 (12.54%)      | 328 (12.07%)        | 1331 (12.42%)        |
| Instrument-Agency  | 504 (6.30%)         | 156 (5.74%)         | 660 (6.16%)          |
| Product-Producer   | 717 (8.96%)         | 231 (8.50%)         | 948 (8.85%)          |
| Content-Container  | 540 (6.75%)         | 192 (7.07%)         | 732 (6.83%)          |
| Entity-Origin      | 716 (8.95%)         | 258 (9.50%)         | 974 (9.09%)          |
| Entity-Destination | 845 (10.56%)        | 292 (10.75%)        | 1137 (10.61%)        |
| Component-Whole    | 941 (11.76%)        | 312 (11.48%)        | 1253 (11.69%)        |
| Member-Collection  | 690 (8.63%)         | 233 (8.58%)         | 923 (8.61%)          |
| Message-Topic      | 634 (7.92%)         | 261 (9.61%)         | 895 (8.35%)          |
| Other              | 1,410 (17.63%)      | 454 (16.71%)        | 1864 (17.39%)        |
| **Total**          | **8,000 (100.00%)** | **2,717 (100.00%)** | **10,717 (100.00%)** |


# Training the model
    $ python train.py --train_dir "Train_file.text"
    
# Testing the model
    $ python evaluate.py --checkpoints_dir "runs/1523902663/checkpoints"
    
   where 1523902663 shall be the file name in which train.py has stored result for latest training of model.
      * **Official Evaluation of SemEval 2010 Task #8**
	1. After evaluation like the example, you can get the "*prediction.txt*" and "*answer.txt*" in "*result*" directory.
	2. Install <U>[perl](https://www.perl.org/get.html)</U>.
	3. Move to <U>*SemEval2010_task8_all_data/SemEval2010_task8_scorer-v1.2*</U>.
        ```bash
        $ cd SemEval2010_task8_all_data/SemEval2010_task8_scorer-v1.2
		```
	4. Check your prediction file format.
		```bash
		$ perl semeval2010_task8_format_checker.pl ../../result/prediction.txt
		```
	5. Scoring your prediction.
		```bash
		$ perl semeval2010_task8_scorer-v1.2.pl ../../result/prediction.txt ../../result/answer.txt
		```
	6. The scorer shows the 3 evaluation reuslts for prediction. The official evaluation result, **(9+1)-WAY EVALUATION TAKING DIRECTIONALITY INTO ACCOUNT -- OFFICIAL**, is the last one. See the [README](SemEval2010_task8_all_data/SemEval2010_task8_scorer-v1.2/README.txt) for more details.
 

    
    
