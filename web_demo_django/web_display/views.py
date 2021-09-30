from django.shortcuts import render

def ueser(request):
    input = request.POST.get('publisher_name')
    #TODO: overwrite output here from DensePhrases model.
    output = input
    print(output)
    return render(request, 'web1.html', {'re': output})

def index(request):
    # with open("aaaa.txt", "r") as f:  # 打开文件
    #     data = f.read()  # 读取文件
    #     print(data)
    return render(request, 'web1.html')
