import glob
import os
import subprocess
import os.path
from plagiarism import compare_file_list
from plagiarism import load_template_text

# run python with sudo

path_exams = "/var/www/html/computer-graphics-exam/examen_1/exams/"
path_imgs = "/var/www/html/computer-graphics-exam/examen_1/img/"

def get_files_of_question(question):
    cuis = glob.glob(path_exams + "/*")
    files = []
    for cui in cuis:
        if os.path.isfile(cui + '/' + question + '.py'):
            files.append(cui + '/' + question + '.py')

    return files

def detect_plagiarism(question, files, path):
    cui = path.split('/')[-1]

    C_COMMENT_REMOVE_PATTERN = "(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)"

    summary_file_name = 'summary.csv'
    result_file_name = 'result.csv'

    template_file_name = question
    remove_pattern = C_COMMENT_REMOVE_PATTERN
    
    template = load_template_text(template_file_name, remove_pattern)

    csv_result = compare_file_list(files, remove_pattern, template, cui)

    #the csv_result is a string
    data_csv = csv_result['summary'].split('\n')
    data = []
    for i in range(1, len(data_csv)):
        if data_csv[i] != "":
            temp = data_csv[i].split(',')

            cui_compare = temp[0].split('/')[-2]
            data.append( [ cui_compare, temp[1] ] )

    #print('aquiii')
    #print(data)

    return data

    #result_file = open(path + '/' +summary_file_name, "w")
    #result_file.write(csv_result['summary'])
    #result_file.close()
 



##########################################################################################
########################### copy images ##################################################
##########################################################################################


imgs = glob.glob(path_imgs + "/*.*")
for img in imgs:
    name = img.split("/")[-1]
    cuis = glob.glob(path_exams+'/*')

    for cui in cuis:
        cmd = 'cp ' + img + ' ' + cui + '/' + name
        #print(cmd)
        os.system(cmd)

print("################################### images copied #############################")

##########################################################################################
########################### execute scripts ##############################################
##########################################################################################
cuis = glob.glob(path_exams+'/*')
for cui in cuis:
    cui_name = cui.split("/")[-1]

    print()
    print( "Evaluating CUI: ", cui_name , "..." )
    print()

    html = " <html> <body> <center> <h3> CUI:" + cui_name + " </h3> <br> <table> "
    html += "<tr>  <td><b>Question</b></td>  <td><b>Code</b></td>  <td><b>Result</b></td> <td><b>Output</b></td> <td><b>Plagiarism</b></td> </tr>"

    questions = glob.glob(path_exams+'/' + cui_name + '/*.py')
    questions.sort()

    for question in questions:    
        question_name = question.split("/")[-1]
        cmd = 'cd ' + cui + ';  python3 ' + question_name
        #print(cmd)
        #os.system(cmd)
        output = subprocess.getoutput(cmd)
  
        question_name_without_ext = question_name.split(".")[0]

        ## read code ####################################
        f = open(question, "r")
        code = f.read()
        f.close()

        ## plagiarism ###################################
        files = get_files_of_question(question_name_without_ext)
        data = detect_plagiarism(question, files, cui)
        plag_table_html = "<table border='1'> <tr> <td> CUI </td> <td> similarity </td> </tr>"
        for row in data:
            plag_table_html += "<tr> <td> " + row[0] +   "</td>  " 
            plag_table_html += "<td> " + row[1] +   "</td> </tr> "
        plag_table_html += "</table>"

        ## process date #################################
        date_time = code.split('\n')[0]
        date = date_time.split(" ")[0]
        date = date.replace("#", '')
        time = date_time.split(" ")[1]
    
        html += "<td> " + question_name_without_ext + "<br> <br>" + date + "<br> " + time + " </td>"
        html += "<td> <textarea rows='30' cols='60'>" + code + "</textarea></td>"
        html += "<td> <img src='" + question_name_without_ext + "_sol.jpg' width='400' height='400'></img> </td> "
        html += "<td width='150px'> " + output + " </td> "
        html += "<td > " + plag_table_html + " </td> </tr>"

    html += " </table> </center> </body></html> "

    f = open(cui + "/results.html", "w")
    f.write(html)
    f.close()

print("################################### scripts executed ##########################")

