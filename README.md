# Usage
Clone the project first.
```
git clone https://github.com/melvynator/DM_FinalProject.git
cd DM_FinalProject
```

Using virtualenv to manage the pip enviroments.

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run data preprocessing.

```
cd jobs
python data_processing.py
```

Back and open the data_exploration.
(Remember run ipython in virtualenv mode or it will be global env.)

```
cd ..
ipython notebook data_exploration/data_exploration.ipynb
```

Click run all in ipython Cell and enjoy the chart!

Finally, you can exit the virtualenv by:
```
deactivate
```

# Demo
[DM_FinalProject](http://nbviewer.jupyter.org/github/melvynator/DM_FinalProject/blob/master/data_exploration/.ipynb_checkpoints/data_exploration-checkpoint.ipynb)