from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import urllib

UPLOAD_FOLDER = '/home1/irteam/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client_id = ""
client_secret = ""


@app.route('/face/search/', methods=["GET", "POST"])
def celeb_search_get():
    if request.method == "GET":
        print(app.config)
        return render_template('home.html')
    else:
        shop: str = request.form.get("shop")
        file = request.files['image']
        file.save("temp.jpg")
        celebs = get_celeb_list()

        celeb_names = list(map(lambda c: c["celebrity"]["value"], celebs))
        resulsts: list = []
        for celeb_name in celeb_names:
            resulsts.extend(get_shop_list(celeb_name=celeb_name, shop=shop)["items"])

        return render_template('home.html', celebs=celebs, resulsts=resulsts)


def get_celeb_list():
    url: str = "https://openapi.naver.com/v1/vision/celebrity"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    files = {'image': open('temp.jpg', 'rb')}
    response = requests.post(url=url, headers=headers, files=files)
    rescode = response.status_code
    # if rescode == 200:
    #     print(response.text)
    # else:
    #     print("Error Code:" + rescode)

    return response.json()["faces"]


def get_shop_list(celeb_name, shop):
    encText = urllib.parse.quote(celeb_name + " " + shop)
    url: str = "https://openapi.naver.com/v1/search/shop?query=" + encText  # json 결과
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    response = requests.get(url=url, headers=headers)
    # print(f"response.status_code : {response.status_code}")
    # print(response.text)
    return response.json()


if __name__ == '__main__':
    app.run(port=8080)

    # IP Open 할 떄
    # app.run(host='0.0.0.0')
