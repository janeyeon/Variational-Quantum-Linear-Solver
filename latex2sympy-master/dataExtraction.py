
h_test_long_name = "htest_tex_long.tex"
h_test_short_name = "htest_tex_short.tex"
specialhtest_short_I_name = "specialhtest_tex_short_I.tex"
specialhtest_long_I_name = "specialhtest_tex_long_I.tex"
specialhtest_short_Z3_name = "specialhtest_tex_short_Z3.tex"
specialhtest_long_Z3_name = "specialhtest_tex_long_Z3.tex"


# Function that import .mat result file into python data format 
def download(file_name = ""):
    with open("./result/" + file_name, "r") as f: 
        file = f.read()
        #print("download file success")
        return file
    

#Function which is divide the downloaded data into longEx and shortEx
#longEx: quantum circuit을 나타내는 표현 
#shortEx: matlab에서 simplify과정을 거친 표현식 

h_test_long = download(file_name=h_test_long_name)
h_test_short = download(file_name=h_test_short_name)
specialh_long_I = download(file_name=specialhtest_long_I_name)
specialh_short_I = download(file_name=specialhtest_short_I_name)
specialh_long_Z3 = download(file_name=specialhtest_long_Z3_name)
specialh_short_Z3 = download(file_name=specialhtest_short_Z3_name)

print("Download file success!")