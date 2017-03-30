LCDB Website
===============

## Purpose

This website will be used by the biologists in LCDB in order to speed up their
scientific research. The end goal is to create three different interconnected
graphs that researchers can use to analyze their NGS data.  This will be done
by first using an MA plot of identify up and down regulated genes.  These genes
can then be selected to be placed into a colocalization heatmap containing ChIP-Seq
data.  Any of the colocalized proteins can then be selected and compared using a
binary heatmap.  In this way a lot of the regulatory information can be explored
by the biologist without having to rely on a bioinformatician.  

Please view image below:

![LCDB Website]( https://github.com/MediciPrime/Repository-Images/blob/master/lcdb.png )

## Setup

### Starting Server

The commands below will initialize the webserver but it will not contain a database.
*Intializing Database* will help you initialize a database and add any necessary data
values.

1. `git clone` the *4C-Workflow* directory into your local directory
2. Install [Miniconda](http://conda.pydata.org/miniconda.html)
3. Create the conda environment with the following command:
   - `conda env create -f environment.yml`
4. Run the newly created environment:
   - `source activate flask`
5. Start web server from the *lcdb_website* directory:
   - `./manage.py runserver

Note: If you want other computer to connect to the web server, determine your local IP
      and enter it in the following way.
      - `./manage.py runserver --host <local IP>`
      
### Intializing Database

1. Initialize the database by running the following commands:
   - `./manage.py db init`
   - `./manage.py db migrate -m "initial migration"`
   - `./manage.py db upgrade`
2. Start the webserver and register an account by clicking on *Log In* in the upper 
   right-hand corner and then on *Click here to register*.
   - Make sure to confirm the account via the confirmation email
3. In the *sample_data* folder make sure to change *your_name* to the name you entered
   for *Username* in the account registration form.
4. With a text editor of your choice, open *update.yaml* and change all occurrences of
   *your_name* to the *username* you entered above. **Case Sensitive**
5. Now add the sample data to the database by running the following command:
   - `./update.py`
   
Your database should now be ready. You should now be able to start the web server with
`./manage.py runserver` and explore it at `http://127.0.0.1:5000/home`.
      
## Moving Parts

A brief description of front-end and back-end files and folders and how they fit into 
the web site as a whole.

### Back-end

The main back-end components include the SQLite server and Flask components that relay
information between back-end and front-end. 

- sample_files/  <-- contains the sample bed files split into *public* and *your_name*
    - make sure to change the *your_name* folder to name you will be using to register
      with the website.
- 

### Front-end

## Acknowledgment
The idea of creating such an interconnected app was thought of by [Ryan Dale](https://github.com/daler).
