import openai
import os, json
from bardapi import Bard
from dotenv import load_dotenv

from guides import *

load_dotenv()

openai.api_key = os.environ["openai_api_key"]
# openai.api_base = "https://chimeragpt.adventblocks.cc/api/v1"

def get_points(topic_sentence, n=5, support=True):
    action = "supports" if support else "opposes"
        
    PROMPT_GEN_POINTS = f"""Give {n} very different and important arguments based on an essay written that directly {action} the topic sentence. Do not give explanations. Do not include the introduction or conclusion. Do not introduce yourself. Follow the format of the example output exactly.

Consider potential arguemnts from the following aspects:
- Social
- Political
- Economic
- Cultural
- Religious
- Environmental
- Historical
- Scientific
- Psychological
- Technological
- Ethical
- Legal
- Moral
- Philosophical
    
EXAMPLE OUTPUT:

- [point]
- [point]
- [point]
...
TOPIC SENTENCE:\n"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_GEN_POINTS + topic_sentence},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"].split("- ")
    res = list(filter(lambda x: len(x) > 0, res))
    res = [x.strip() for x in res]
    res = [x if "\n" not in x else x.split("\n")[0].strip() for x in res]
    return res

def get_example(topic_sentence, point, old_example="", feedback=""):
          
    web_context = Bard().get_answer(f"""What is one recent examples that support the argument about the topic statement?

ARGUMENT:
{point}

TOPIC STATEMENT:
{topic_sentence}""")['content']
    PROMPT_GEN_EXAMPLE = f"""Give a few specific examples with names supporting
the argument for the topic sentence, optionally using additional examples retrieved from the web as context.

Describe only the examples. Do not explain. 

ARGUMENT:
{point}

TOPIC SENTENCE:
{topic_sentence}

ADDITIONAL EXAMPLES FROM THE WEB:
{web_context}

Example output:
Example 1: [Description of example 1]
Example 2: [Description of example 2]"""
    
    PROMPT_GEN_EXAMPLE_F = f"""Give a few specific examples with names supporting
the argument for the topic sentence, optionally using additional examples retrieved from the web as context.

Describe only the examples. Do not explain. 

ARGUMENT:
{point}

TOPIC SENTENCE:
{topic_sentence}

ADDITIONAL EXAMPLES FROM THE WEB:
{web_context}

Take into account these previous specific examples: {old_example}
Take into account the feedback given for this previous specific examples: {feedback}

Example output:
1. [Description of example 1]
2. [Description of example 2]"""
    if feedback.strip() != "" and old_example.strip() != "":
        PROMPT_GEN_EXAMPLE = PROMPT_GEN_EXAMPLE_F
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_GEN_EXAMPLE},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res

def get_feedback_point(topic_sentence, point):
    PROMPT_FEEDBACK_POINT = f"""Provide feedback on the following main point or argument based on the topic sentence. Suggest an improvement for the main point or argument. 
Argument: {point}
Topic sentence: {topic_sentence}"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_FEEDBACK_POINT},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res

def get_feedback_example(topic_sentence, example, point):
    PROMPT_FEEDBACK_EXAMPLE = f"""Provide feedback on the following examples supporting the argument about the topic sentence. Suggest better examples to support the argument.
Examples: {example}
Argument: {point}
Topic sentence: {topic_sentence}"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_FEEDBACK_EXAMPLE},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res

def get_paragraph(topic_sentence, point, example, old_para="", feedback=""):
    PROMPT_GEN_PARA = f"""Generate a body paragraph for an essay with the title based on the argument and the example. Use concise and complex language.

Closely follow the guide to generate a body paragraph.

GUIDE TO WRITE A BODY PARAGRAPH:
{BODY_GUIDE}

ESSAY TITLE:
{topic_sentence}

ARGUMENT:
{point}

EXAMPLE:
{example}"""

    PROMPT_GEN_PARA_F = f"""Generate a body paragraph for an essay with the title based on the argument and the example. Use concise and complex language.

Closely follow the guide to generate a body paragraph.

GUIDE TO WRITE A BODY PARAGRAPH:
{BODY_GUIDE}

Improve on this body paragraph: {old_para}
Take into account the feedback given for this body paragraph: {feedback}
ESSAY TITLE:
{topic_sentence}

ARGUMENT:
{point}

EXAMPLE:
{example}"""
    if feedback.strip() != "" and old_para.strip() != "":
        PROMPT_GEN_PARA = PROMPT_GEN_PARA_F

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_GEN_PARA},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res

def get_feedback_paragraph(topic_sentence, paragraph):
    PROMPT_FEEDBACK_PARA = f"""Give feedback on how convincing and well-written the body paragraph was, and how well it followed the guide.

GUIDE:
{BODY_GUIDE}

TOPIC SENTENCE:
{topic_sentence}

BODY PARAGRAPH:
{paragraph}"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_FEEDBACK_PARA},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res

def get_conclusion(topic_sentence, main_points, old_conclusion="", feedback=""):
    main_points = [f"- {x}" for x in main_points]
    points = "\n".join(main_points)
    PROMPT_GEN_CONCLUSION = f"""Generate a one paragraph conclusion for an essay based on the title and main points. Use concise and complex language. 

Closely follow the guide to generate a one paragraph conclusion.

GUIDE TO WRITE AN CONCLUSION:
{CONCLUSION_GUIDE}

TITLE:
{topic_sentence}

MAIN POINTS:
{points}"""
    
    PROMPT_GEN_CONCLUSION_F = f"""Generate a one paragraph conclusion for an essay based on the title and main points. Use concise and complex language. 

Closely follow the guide to generate a one paragraph conclusion.

GUIDE TO WRITE AN CONCLUSION:
{CONCLUSION_GUIDE}

Improve on this conclusion: {old_conclusion}
Take into account the feedback given for this conclusion: {feedback}
    
TITLE:
{topic_sentence}

MAIN POINTS:
{points}"""
    if feedback.strip() != "" and old_conclusion.strip() != "":
        PROMPT_GEN_CONCLUSION = PROMPT_GEN_CONCLUSION_F
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_GEN_CONCLUSION},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res


def get_feedback_conclusion(topic_sentence, conclusion, main_points):
    main_points = [f"- {x}" for x in main_points]
    points = "\n".join(main_points)
    PROMPT_FEEDBACK_CONCLUSION = f"""Give feedback on how convincing and well-written the one paragraph conclusion was, and how well it followed the guide.

GUIDE:
{CONCLUSION_GUIDE}

TOPIC SENTENCE:
{topic_sentence}

CONCLUSION:
{conclusion}

MAIN POINTS:
{points}"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_FEEDBACK_CONCLUSION},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res



def get_introduction(topic_sentence, main_points, old_intro="", feedback=""):
    main_points = [f"- {x}" for x in main_points]
    points = "\n".join(main_points)
    PROMPT_GEN_INTRO = f"""Generate a one paragraph introduction for an essay based on the title and main points, and guide to write an introduction. Use concise and complex language.

Closely follow the guide to generate a one paragraph introduction.

GUIDE TO WRITE AN INTRODUCTION:
{INTRO_GUIDE}
    
TITLE:
{topic_sentence}

MAIN POINTS:
{points}"""
    
    PROMPT_GEN_INTRO_F = f"""Generate a one paragraph introduction for an essay based on the title and main points, and guide to write an introduction. Use concise and complex language.

Improve on this introduction: {old_intro}
Take into account the feedback given for this introduction: {feedback}

Closely follow the guide to generate a one paragraph introduction.

GUIDE TO WRITE AN INTRODUCTION:
{INTRO_GUIDE}
    
TITLE:
{topic_sentence}

MAIN POINTS:
{points}"""
    
    if feedback.strip() != "" and old_intro.strip() != "":
        PROMPT_GEN_INTRO = PROMPT_GEN_INTRO_F

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_GEN_INTRO},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res


def get_feedback_introduction(topic_sentence, intro, main_points):
    main_points = [f"- {x}" for x in main_points]
    points = "\n".join(main_points)
    PROMPT_FEEDBACK_INTRO = f"""Give feedback on how convincing and well-written the one paragraph introduction was, and how well it followed the guide.

GUIDE:
{INTRO_GUIDE}

TOPIC SENTENCE:
{topic_sentence}

INTRODUCTION:
{intro}

MAIN POINTS:
{points}"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": PROMPT_FEEDBACK_INTRO},
        ],
        temperature=0,
    )
    res = response["choices"][0]["message"]["content"]
    return res
