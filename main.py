import gradio as gr
from utils import *

with gr.Blocks(theme="gstaff/xkcd", title="Esslay") as demo:

    gr.HTML(
        """

        <h1 style="font-size: 300%"><b>Esslay</b></h1>

        <h3 style="color: gray">Slay your essays with Esslay<h3>
        <p style="font-size: 83%; color: gray">Read the essay guide <a href="https://gp.sg/general-paper-essay-examples-notes.pdf" target="_blank">here<a/></p>

        """
    )

    with gr.Row():
        qn_box = gr.Textbox(label="Essay question", scale=6)
        submit_btn = gr.Button("Submit", scale=1)


    btn_names = [f"{i}: For" for i in range(1,6)]
    btn_names += [f"{i}: Against" for i in range(6,11)]
    # print(btn_names)
    point_btns = [None] * 10
    example_gen_btns = [None] * 10
    example_feedback_btns = [None] * 10
    para_feedback_btns = [None] * 10
    para_gen_btns = [None] * 10
    point_textboxes = [None] * 10
    point_feedback = [None] * 10
    fixed_point_textboxes = [None] * 10
    example_textboxes = [None] * 10
    example_feedback = [None] * 10
    paragraph_textboxes = [None] * 10
    paragraph_feedback = [None] * 10

    # points = []
    # point_feedbacks = []
    # paragraphs = []
    # paragraph_feedbacks = []
    # examples = []
    # example_feedbacks = []

    with gr.Column(visible=False) as output_col:
        with gr.Tab("Points overview"):
            for i, x in enumerate(btn_names):
                fixed_point_textboxes[i] = gr.Textbox(label=f"Point {x}")
            with gr.Row():
                intro_textbox = gr.Textbox(label="Introduction", interactive=True)
                intro_feedback = gr.Textbox(label="Introduction feedback", interactive=False)
            with gr.Row():
                intro_gen_btn = gr.Button("Generate introduction")
                intro_feedback_btn = gr.Button("Get feedback on introduction")

            with gr.Row():
                conclusion_textbox = gr.Textbox(label="Conclusion", interactive=True)
                conclusion_feedback = gr.Textbox(label="Conclusion feedback", interactive=False)
            with gr.Row():
                conclusion_gen_btn = gr.Button("Generate conclusion")
                conclusion_feedback_btn = gr.Button("Get feedback on conclusion")
            
        for i, x in enumerate(btn_names):
            with gr.Tab(f"Point {x}"):
                with gr.Column():
                    with gr.Row():
                        point_textboxes[i] = gr.Textbox(label=f"Point {x}", interactive=True)
                        point_feedback[i] = gr.Textbox(label="Point feedback", interactive=False)
                    with gr.Row():
                        point_btns[i] = gr.Button("Get feedback on point")
                    with gr.Row():
                        example_textboxes[i] = gr.Textbox(label="Example", interactive=True)
                        example_feedback[i] = gr.Textbox(label="Example feedback", interactive=False)
                    with gr.Row():
                        example_gen_btns[i] = gr.Button("Generate example")
                        example_feedback_btns[i] = gr.Button("Get feedback on example")
                    with gr.Row():
                        paragraph_textboxes[i] = gr.Textbox(label="Paragraph", interactive=True)
                        paragraph_feedback[i] = gr.Textbox(label="Paragraph feedback", interactive=False)
                    with gr.Row():
                        para_gen_btns[i] = gr.Button("Generate paragraph")
                        para_feedback_btns[i] = gr.Button("Get feedback on paragraph")
                


    def submit(topic_sentence):
        if len(topic_sentence) == 0:
            raise gr.Error("Please enter an essay question.")
        
        # call api
        pos_points = get_points(topic_sentence, support=True)
        neg_points = get_points(topic_sentence, support=False)
        points = pos_points + neg_points
        res = {x:gr.update(value=points[i], lines=len(points[i])//97 + (1 if len(points[i])%97 else 0))  for i, x in enumerate(point_textboxes)}
        res2 = {x:points[i]  for i, x in enumerate(fixed_point_textboxes)}
        return {
            output_col: gr.update(visible=True),
            **res,
            **res2
        }
    
    submit_btn.click(
        submit,
        [qn_box],
        [output_col, *point_textboxes, *fixed_point_textboxes],
    )

    def gen_point_feedback(i):
        def feedback_point(topic_sentence, point):
            if len(point) == 0:
                raise gr.Error("Please enter an point.")
            if len(topic_sentence) == 0:
                raise gr.Error("Please enter an essay question.")
            res = get_feedback_point(topic_sentence=topic_sentence, point=point)
            # res = f"TEST EV PT {i}"
            return{
                point_feedback[i]: res
            }
        return feedback_point
    
    for i in range(10):
        func = gen_point_feedback(i)
        point_btns[i].click(
            func,
            [qn_box, point_textboxes[i]],
            [point_feedback[i]]
        )

    def gen_example_gen(i):
        def gen_example(topic_sentence, point, old_example="", feedback=""):
            if len(point) == 0:
                raise gr.Error("Please enter an point.")
            if len(topic_sentence) == 0:
                raise gr.Error("Please enter an essay question.")
            res = get_example(topic_sentence=topic_sentence, point=point, old_example=old_example, feedback=feedback)
            # res = f"TEST EG {i}"
            return{
                example_textboxes[i]: res
            }
        return gen_example
    
    for i in range(10):
        func = gen_example_gen(i)
        example_gen_btns[i].click(
            func,
            [qn_box, point_textboxes[i], example_textboxes[i], example_feedback[i]],
            [example_textboxes[i]]
        )
    
    def gen_example_feedback(i):
        def feedback_example(topic_sentence, example, point):
            if len(point) == 0:
                raise gr.Error("Please enter an point.")
            if len(example) == 0:
                raise gr.Error("Please enter an example.")
            if len(topic_sentence) == 0:
                raise gr.Error("Please enter an essay question.")
            res = get_feedback_example(topic_sentence=topic_sentence, example=example, point=point)
            # res = f"TEST EV {i}"
            return{
                example_feedback[i]: res
            }
        return feedback_example
    
    for i in range(10):
        func = gen_example_feedback(i)
        example_feedback_btns[i].click(
            func,
            [qn_box, example_textboxes[i], point_textboxes[i]],
            [example_feedback[i]]
        )

    def gen_para_gen(i):
        def gen_para(topic_sentence, point, example, old_para="", feedback=""):
            if len(point) == 0:
                raise gr.Error("Please enter an point.")
            if len(topic_sentence) == 0:
                raise gr.Error("Please enter an essay question.")
            if len(example) == 0:
                raise gr.Error("Please enter an example.")
            res = get_paragraph(topic_sentence=topic_sentence, point=point, example=example, old_para=old_para, feedback=feedback)
            # res = f"TEST EG PARA {i}"
            return{
                paragraph_textboxes[i]: res
            }
        return gen_para
    
    for i in range(10):
        func = gen_para_gen(i)
        para_gen_btns[i].click(
            func,
            [qn_box, point_textboxes[i], example_textboxes[i], paragraph_textboxes[i], example_feedback[i]],
            [paragraph_textboxes[i]]
        )

    def gen_para_feedback(i):
        def feedback_para(topic_sentence, paragraph):
            if len(paragraph) == 0:
                raise gr.Error("Please enter an paragraph.")
            if len(topic_sentence) == 0:
                raise gr.Error("Please enter an essay question.")
            res = get_feedback_paragraph(topic_sentence=topic_sentence, paragraph=paragraph)
            # res = f"TEST EV PARA {i}"
            return{
                paragraph_feedback[i]: res
            }
        return feedback_para
    
    for i in range(10):
        func = gen_para_feedback(i)
        para_feedback_btns[i].click(
            func,
            [qn_box, paragraph_textboxes[i]],
            [paragraph_feedback[i]]
        )

    def gen_intro(topic_sentence, *points, old_intro="", feedback=""):
        if len(topic_sentence) == 0:
            raise gr.Error("Please enter an essay question.")
        res = get_introduction(topic_sentence=topic_sentence, main_points=list(points), old_intro=old_intro, feedback=feedback)
        # res = f"TEST EG INTRO {i}"
        return{
            intro_textbox: res
        }
    
    intro_gen_btn.click(
        gen_intro,
        [qn_box, *fixed_point_textboxes, intro_textbox, intro_feedback],
        [intro_textbox]
    )
    
    def gen_intro_feedback(topic_sentence, intro, *points):
        if len(intro) == 0:
            raise gr.Error("Please enter an introduction.")
        if len(topic_sentence) == 0:
            raise gr.Error("Please enter an essay question.")
        res = get_feedback_introduction(topic_sentence=topic_sentence, intro=intro, main_points=list(points))
        # res = f"TEST EV INTRO {i}"
        return{
            intro_feedback: res
        }
    
    intro_feedback_btn.click(
        gen_intro_feedback,
        [qn_box, intro_textbox, *fixed_point_textboxes],
        [intro_feedback]
    )

    def gen_conclusion(topic_sentence, *points, old_conclusion="", feedback=""):
        if len(topic_sentence) == 0:
            raise gr.Error("Please enter an essay question.")
        res = get_conclusion(topic_sentence=topic_sentence, main_points=list(points), old_conclusion=old_conclusion, feedback=feedback)
        # res = f"TEST EG INTRO {i}"
        return{
            conclusion_textbox: res
        }
    
    conclusion_gen_btn.click(
        gen_conclusion,
        [qn_box, *fixed_point_textboxes, conclusion_textbox, conclusion_feedback],
        [conclusion_textbox]
    )
    
    def gen_conclusion_feedback(topic_sentence, conclusion, *points):
        if len(conclusion) == 0:
            raise gr.Error("Please enter an introduction.")
        if len(topic_sentence) == 0:
            raise gr.Error("Please enter an essay question.")
        res = get_feedback_conclusion(topic_sentence=topic_sentence, conclusion=conclusion, main_points=list(points))
        # res = f"TEST EV INTRO {i}"
        return{
            conclusion_feedback: res
        }
    
    conclusion_feedback_btn.click(
        gen_conclusion_feedback,
        [qn_box, conclusion_textbox, *fixed_point_textboxes],
        [conclusion_feedback]
    )

    # def show_example(i):
    #     example_vis[i] = not example_vis[i]
    #     if example_vis[i]:
    #         return {
    #             example_boxes[i]: gr.update(visible=False),
    #             btns[i]: "Show example",
    #         }
    #     return {
    #         example_boxes[i]: gr.update(visible=True),
    #         btns[i]: "Hide example",
    #     }
    
    # on button click show example
    # funcs = [None] * 10
    # for i in range(10):
    #     funcs[i] = lambda: show_example(i)
    #     btns[i].click(
    #         funcs[i],
    #         [],
    #         [*example_boxes, *btns],
    #     )


demo.launch(share=True)