# SI507-FinalProject-shewang
This is the final project for umich SI507
Main contents of the project:
1. crawling data from www.amazon.com and www.bestbuy.com. The information crawled includes basic information 
   of computer and customer reviews. I fetched four kinds of computer: macbook air, macbook pro, surface and thinkpad.
   If you would like to fetch other kinds of computer, run fetch_data.py and add fetch_all(product_name) in the main section.
   Sometimes the file may fail and usually it is because the BeautifulSoup cannot analyze www.amazon.com html file well.
   In this situation, change the number of i in fetch_amazon function.

2. Forming database using SQL. The database includes two tables: information and customer.
   If you want to fetch other kinds of computer and forming the database, run forming_db.py and add the information of the data
   you fatched following the formate in the main section.

3. Managing data. Rating.py is used for managing data. It includes 
   a). Getting the histogram of rating of one kind of computer. 
   b). Getting the average rating through time curve of one kind of computer. b).Getting the title of customer review of one
       kind of computer. Just calling the related function by computer name.

4. To do unit test, call test_final.py.

5. Using flask to do data presentation. Run present.py. If you fetch your own data, don't forget to modify present.py


Other files:
1. Before you run the project:
   a). mkdir a new file_folder, cd into the folder and create a virtual enviroment by command "virtualenv project".
   b). source into the enviroment by command "source project/bin/activate"
   c). install the pakage you need in this project by command "pip install -r requirements.txt"
2. templates
   template folder includes the html templates you would use.
3. static
   After you getting the image from rating.py, add image to static folder
4. model.py
   Includes the model you will use when calling flask. Add name if fetch new kind of computer.
