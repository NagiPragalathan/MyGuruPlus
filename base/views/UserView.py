from django.shortcuts import render
from base.models import PathManager, FolderManager, McqQuestionBase

def ListCourse(request, path):
    user = request.user
    temp = []
    temp1=[]
    Files = PathManager.objects.filter(user_id=user, path=path)
    folders = FolderManager.objects.filter(user_id=user, path=path).order_by('FolderName')
    mcq_questions = McqQuestionBase.objects.filter(user_id=user, path=path, question_type="MCQ")
    para_mcq_questions = McqQuestionBase.objects.filter(user_id=user, path=path, question_type="PARA")
    unique_para_categories_list = list(para_mcq_questions.values_list('quest_id', flat=True).distinct())
    unique_categories_list = list(mcq_questions.values_list('category', flat=True).distinct())
    Files = sorted(Files, key=lambda x: x.file.name)
    print(unique_para_categories_list)
    for file in Files:
        file_extension = file.file.name.split('.')[-1].lower()
        if file_extension.lower() in ['jpg', 'png', 'gif', 'jpeg', 'svg', 'webp', 'ico']:
            file.icon_path = file.file.url  # Adjust the path as needed
        else:
            file.icon_path = f'/static/images/Folders/{file_extension}.png'  # Adjust the path as needed
        file.type = file_extension
        file.title_name = file.title + "." + file_extension
    
    category = [i.FolderName for i in FolderManager.objects.filter(user_id=user, path="root").order_by('FolderName')]

    for i in unique_categories_list:
        print(i)
        # Create a new dictionary in each iteration
        current_mcq_out = {}
        current_mcq_out['name'] = i
        current_mcq_out['icon'] = f'/static/images/Folders/mcq.jpg'
        temp.append(current_mcq_out)
    for i in unique_para_categories_list:
        print(i)
        # Create a new dictionary in each iteration
        current_mcq_out = {}
        current_mcq_out['name'] = i
        current_mcq_out['icon'] = f'/static/images/Folders/para_mcq.png'
        temp1.append(current_mcq_out)
        
    out = ""
    path_list = []
    out_path = {}
    for i in path.split("."):
        out = out + i + "."
        path_list.append(out)
    path_list = [s[:-1] if s.endswith('.') else s for s in path_list]
    for i,j in zip(path_list,path.split('.')):
        out_path[j] = i
    
    if path == 'root':
        return render(request, 'UserView/ListCourse.html', {'path':path,'path_alter':path.replace(".", "/"),
                                                         'path_list':out_path,'folders': folders, 'files': Files,
                                                         'category':category, 'mcq':temp,'mcq_para':temp1})
    else:
        return render(request, 'UserView/ListCourse_Folder.html', {'path':path,'path_alter':path.replace(".", "/"),
                                                         'path_list':out_path,'folders': folders, 'files': Files,
                                                         'category':category, 'mcq':temp,'mcq_para':temp1})
        
def take_quiz(request, path):
    mcq_questions = McqQuestionBase.objects.filter(user_id=request.user)
    out_mcq = []
    for i in mcq_questions:
        if "," in i.copy_qust_path:
            if path in i.copy_qust_path.split(", "):
                out_mcq.append(i)
        else:
            if path == i.copy_qust_path:
                out_mcq.append(i)
    questions = []
    options = []

    out = {"instructions":mcq_questions[0].instructions,"questions":[{'id':question.id,'question': question.question,'options': question.options,'explain':question.explain,"correctAnswer":question.correct_answer,"last_updated_date":question.last_updated_date.strftime('%Y-%m-%d %H:%M:%S')} for question in out_mcq]}
    for question in out_mcq:
        questions.append(question.question)
        options.append(question.options)
    print(questions, options)
    return render(request, "UserView/TakeQuiz.html",{'questions':questions,'options':options})

