
h_test_long_name = "htest_tex_long.tex"
h_test_short_name = "htest_tex_short.tex"
specialh_short_name = "specialh_tex_short.tex"
specialh_long_name = "specialh_tex_long.tex"


# Function that import .mat result file into python data format 
def download(file_name = ""):
    with open("./result/" + file_name, "r") as f: 
        file = f.read()
        print("download file success")
        return file
    

#Function which is divide the downloaded data into longEx and shortEx
#longEx: quantum circuit을 나타내는 표현 
#shortEx: matlab에서 simplify과정을 거친 표현식 

h_test_long_ex = download(file_name=h_test_long_name)
h_test_short_ex = download(file_name=h_test_short_name)
specialh_long_ex = download(file_name=specialh_long_name)
specialh_short_ex = download(file_name=specialh_short_name)
