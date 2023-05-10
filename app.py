import gradio as gr
import requests
import openai
import random

class main(object):



    def __new__(cls, *args, **kwargs):
        if not hasattr(main,"_instance"):
            main._instance = object.__new__(cls)
            return main._instance

    def __init__(self):
        if not hasattr(main,"_first_init"):
            main._first_init = True
            main.auth_list = {
                'admin': '123456'
            }
            main.ban_words = [
                'fighting',
                'smoking'
            ]
            # if you have OpenAI API key as a string, enable the below
            openai.api_key =""
            main.prompt = """
                Please give me a description.
            """

            self.configGradioPara()

    def openai_create(self, prompt):
        """Function to create a response

        Args:
            prompt (_type_): str
                piece of text or a set of instructions that is provided as input
        Returns:
            str: text
        """
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " Bot:"],
        )

        return response.choices[0].text


    def login(self, acc, pwd):
        if len(acc) ==0 or len(pwd)==0:
            return '', 'Account or password is empty.', 'False'
        else:
            if acc in self.auth_list:
                if pwd == self.auth_list[acc]:
                    # Clear the password box with '******'
                    return '******', 'Welcome back, '+ acc, 'True'
                else:
                    # pwd is not matched
                    return '', 'Please check your account or password.', 'False'
            else:
                # acc is not in the list
                return '', 'Please check your account or password.', 'False'

    def check_ban_words(self, word):
        if word not in self.ban_words:
            # Allowed
            return True
        else:
            # Not Allowed
            return False

    def get_prompt(self,loginState, input):
        if loginState != "True":
            return 'Please login first.', None
        else:
            if len(input) == 0:
                # Description is empty
                missing_propmpt_msg = "Please give me a propmpt."
                missing_img = 'D:\\Programme\\Diffusion\\SE\\missingword_sample.jpg'
                # No Description in Chat Bot
                return missing_propmpt_msg, missing_img
            else:
                if self.check_ban_words(input) != True:
                    # Word in banned list
                    ban_png = 'D:\\Programme\\Diffusion\\SE\\ban.png'
                    output = 'Key word is in not allowed.'
                    return output, ban_png
                else:
                    """Function to build Gradio Application

                    Args:
                        input (_type_): str
                            text from user
                        history (_type_): str
                            stores the state of the current gradio application
                            | stores knowledge of context of memory what is happening in past as well
                    Returns:
                        tuple: output and state
                    """
                    output = self.openai_create(input)
                    return output, None



    def clean_content(self):
        # Output the empty string to two component and clear the image box
        return '', '', None
    
    def gen_image(self, loginState, input):
        if loginState != "True":
            return 'Please login first.', None
        else:
            print(input)
            if len(input) == 0:
                    # Description is empty
                    missing_propmpt_msg = "Please give me a propmpt."
                    missing_img = 'D:\\Programme\\Diffusion\\SE\\missingword_sample.jpg'
                    # No Description in Chat Bot
                    return missing_propmpt_msg, missing_img
            else:
                if self.check_ban_words(input) != True:
                    # Word in banned list
                    ban_png = 'D:\\Programme\\Diffusion\\SE\\ban.png'
                    output = 'Key word is in not allowed.'
                    return output, ban_png
                else:
                    headers_payload = {
                        'Host': '127.0.0.1:7860',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Referer': 'http://127.0.0.1:7860/?__theme=dark',
                        'Content-Length': '1696',
                        'Origin': 'http://127.0.0.1:7860',
                        'Connection': 'keep-alive',
                        'Cookie': '_ga=GA1.1.1794975810.1680778101',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
                        'Accept': '"/"',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Content-Type': 'application/json'
                    }

                    postive_input = input
                    negative_input = ""
                    json_payload = {
                        "fn_index": 102,
                        "data": [
                            postive_input,
                            negative_input,
                            "None",
                            "None",
                            20,
                            "DPM++ 2M",
                            False,
                            False,
                            1,
                            1,
                            7,
                            712843927,
                            -1,
                            0,
                            0,
                            0,
                            False,
                            512,
                            512,
                            False,
                            0.7,
                            0,
                            0,
                            "None",
                            0.9,
                            5,
                            "0.0001",
                            False,
                            "None",
                            "",
                            0.1,
                            False,
                            False,
                            False,
                            False,
                            "",
                            "Seed",
                            "",
                            "Nothing",
                            "",
                            True,
                            False,
                            False,
                            None,
                            "",
                            ""
                        ],
                        "session_hash": "5h7tkn1ch54"
                    }

                    img = requests.post('http://127.0.0.1:7860/run/predict/', headers=headers_payload, json=json_payload)
                    img_path = img.json()['data'][0][0]['name']
                    return input, img_path

            
    def configGradioPara(self):
        with gr.Blocks(css="button#clean_btn {background-color: red}") as demo:
            gr.Markdown(
                """<h1><center>MUST Software Engineering</center></h1>
            """
            )

            # Login State
            loginState = gr.State('False')
                
            with gr.Accordion(label="Login", open=False):
                with gr.Row():
                    with gr.Column(scale=12):
                        acc = gr.Textbox(show_label=True, label="Account").style(container=True)
                    with gr.Column(scale=12):
                        pwd = gr.Textbox(show_label=True, label="Password").style(container=True)
                    with gr.Column(scale=12):
                        # variant="primary" - Change Color
                        loginBtn = gr.Button("♻️ Login", variant="primary")

            with gr.Row():
                with gr.Column(scale=1, min_width=150):
                    input_box = gr.Textbox(label="Description",placeholder=self.prompt)
                    pre_gen_input_box = gr.Textbox(label="Prompt",placeholder="")
                    with gr.Row():
                        clear_button = gr.Button("🗑️ Clear", elem_id="clean_btn")
                        # variant="primary" - Change Color
                        submit_button = gr.Button("🚀 Send", elem_id="submit_btn", variant="primary")

                with gr.Column(scale=1, min_width=150):
                    img_box = gr.Image()
                    # variant="primary" - Change Color
                    txt_to_img_btn = gr.Button("🔄 Generate Image from Prompt", variant="primary")
            
            loginBtn.click(self.login, inputs=[acc, pwd], outputs=[pwd, input_box, loginState])
            clear_button.click(self.clean_content, outputs=[input_box, pre_gen_input_box, img_box])
            submit_button.click(self.get_prompt, inputs=[loginState, input_box], outputs=[pre_gen_input_box, img_box])
            txt_to_img_btn.click(self.gen_image, inputs=[loginState, pre_gen_input_box], outputs=[pre_gen_input_box, img_box])



        demo.launch(server_name="0.0.0.0", server_port=7988)

if __name__ == '__main__':
    root = main()