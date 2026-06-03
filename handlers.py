from button import button_start, button_correct_your_favourite_team
from all_teams import teams, teams_url, teams_url_results
from started_matches import started_matches
from upcoming_match import upcoming_match
from match_results import match_results
from aiogram.filters import Command
from db import read_db, write_db
from config import db_file_name
from aiogram import F, Router


router = Router()


#------------------------------------------------------------------------------------


@router.message(Command('start'))
async def hello_world(message):
    data_base = read_db(db_file_name)
    isactive = False
    for i in data_base:
        if i["id"] == message.from_user.id:
            isactive = True
            break
    if isactive == False:
        await message.answer("Hi, This bot can\n\n1) Alerts about upcoming matches\n2) Alerts about started matches\n3) Match results\n4) Select your favorite clubs (to receive alerts only for them)\n\nFirst, fill out a short questionnaireplease write your name.")
        data_base.append({"id" :  message.from_user.id, "name" :  "", "age" : "", "favorite_teams" : []})
        for i in data_base:
            if i["id"] == message.from_user.id:
                i["state"] = "wait name"
        write_db(db_file_name, data_base)
    else:
        await message.answer("Hi")


@router.message(lambda message:any([True for i in read_db(db_file_name) if i["id"] == message.from_user.id and i["state"] == "wait name"]))
async def hello_world(message):
    data_base = read_db(db_file_name)
    for i in data_base:
        if i["id"] == message.from_user.id:
            i["name"] = str(message.text)
            i["state"] = "wait age"
    await message.answer("please write your age")
    write_db(db_file_name, data_base)


@router.message(lambda message:any([True for i in read_db(db_file_name) if i["id"] == message.from_user.id and i["state"] == "wait age"]))
async def hello_world(message):
    data_base = read_db(db_file_name)
    for i in data_base:
        if i["id"] == message.from_user.id:
            i["age"] = str(message.text)
            i["state"] = "wait team"
    text = """Available football teams :\n\n"""
    for i in teams:
        text = text + f"- `{i}`\n"
    await message.answer(text + "\nPlease write down your favorite football team from this list", parse_mode="Markdown")
    write_db(db_file_name, data_base)


@router.message(lambda message:any([True for i in read_db(db_file_name) if i["id"] == message.from_user.id and i["state"] == "wait team"]))
async def hello_world(message):
    data_base = read_db(db_file_name)
    for i in data_base:
        if i["id"] == message.from_user.id:
            if str(message.text) in teams:
                if str(message.text) not in i["favorite_teams"]:
                    i["favorite_teams"].append(str(message.text))
                    i["state"] = ""
                    text = ""
                    for favourite_team in i["favorite_teams"]:
                        text = text + favourite_team + " "
                    await message.answer(f"Your form is completed!\n\nName: {i["name"]}\nFavorite teams: {text}\n\nSelect the bot function", reply_markup=button_start)
                else:
                    await message.answer("Your team already in list")
                    i["state"] = "wait team"
            else:
                await message.answer("try again")
                i["state"] = "wait team"
    write_db(db_file_name, data_base)


#------------------------------------------------------------------------------------


@router.message(F.text == "correct your favourite team")
async def hello_world(message):
    data_base = read_db(db_file_name)
    text = "Choose what you want to do, your teams : \n \n"
    for i in data_base:
        if i["id"] == message.from_user.id:
            for favourite_team in i["favorite_teams"]:
                text = text + f"- `{favourite_team}`\n"
        await message.answer(text, parse_mode="Markdown", reply_markup=button_correct_your_favourite_team)
    write_db(db_file_name, data_base)


@router.message(F.text == "add team")
async def hello_world(message):
    data_base = read_db(db_file_name)
    text = """Available football teams : \n \n"""
    for i in teams:
        text = text + f"- `{i}` \n"
    await message.answer(text + "\nPlease write another football team from this list", parse_mode="Markdown")
    for i in data_base:
        if i["id"] == message.from_user.id:
            i["state"] = "wait team2"
    write_db(db_file_name, data_base)

    
@router.message(lambda message:any([True for i in read_db(db_file_name) if i["id"] == message.from_user.id and i["state"] == "wait team2"]))
async def hello_world(message):
    data_base = read_db(db_file_name)
    for i in data_base:
        if i["id"] == message.from_user.id:
            if str(message.text) in teams:
                if str(message.text) not in i["favorite_teams"]:
                    i["favorite_teams"].append(str(message.text))
                    i["state"] = ""
                    text = ""
                    for favourite_team in i["favorite_teams"]:
                        text = text + f"-{favourite_team}\n"
                    await message.answer(f"Your favorite teams:\n\n{text}", reply_markup=button_correct_your_favourite_team)
                else:
                    await message.answer("Your team already in list")
                    i["state"] = "wait team2"
            else:
                await message.answer("try again")
                i["state"] = "wait team2"
    write_db(db_file_name, data_base)

    
@router.message(F.text == "delete team")
async def hello_world(message):
    data_base = read_db(db_file_name)
    text = "Enter the command you want to remove from list : \n \n"
    for i in data_base:
        if i["id"] == message.from_user.id:
            for favourite_team in i["favorite_teams"]:
                text = text + f"- `{favourite_team}`\n"
    await message.answer(text, parse_mode="Markdown", reply_markup=button_correct_your_favourite_team)
    for i in data_base:
        if i["id"] == message.from_user.id:
            i["state"] = "wait team3"
    write_db(db_file_name, data_base)


@router.message(lambda message:any([True for i in read_db(db_file_name) if i["id"] == message.from_user.id and i["state"] == "wait team3"]))
async def hello_world(message):
    data_base = read_db(db_file_name)
    text = ""
    for i in data_base:
        if i["id"] == message.from_user.id:
            if message.text not in i["favorite_teams"]:
                await message.answer("Your team already is not in list")
                i["state"] = "wait team3"
            else:
                for favourite_team in i["favorite_teams"]:
                    if favourite_team != message.text:
                        text = text + f"-{favourite_team}\n"
                i["favorite_teams"].remove(message.text)
                i["state"] = " "
    await message.answer(f"Yor favorite teams:\n\n{text}", reply_markup=button_start)
    write_db(db_file_name, data_base)


#------------------------------------------------------------------------------------


@router.message(F.text == "upcoming match for your favourite teams")
async def hello_world(message):
    data_base = read_db(db_file_name)
    url = []
    for i in data_base:
        if i["id"] == message.from_user.id:
            for teamuy in i["favorite_teams"]:
                url.append(teams_url[teamuy])
    text = ""
    for i in url:
        text = text + str(upcoming_match(i))
    await message.answer(text, reply_markup=button_start)
    write_db(db_file_name, data_base)
    

#------------------------------------------------------------------------------------


@router.message(F.text == "match results")
async def hello_world(message):
    data_base = read_db(db_file_name)
    text = """Available football teams : \n \n"""
    for i in teams:
        text = text + f"- `{i}` \n"
    await message.answer(text + "\nPlease write football team from this list", parse_mode="Markdown")
    for i in data_base:
        if i["id"] == message.from_user.id:
            i["state"] = "wait team4"
    write_db(db_file_name, data_base)


@router.message(lambda message:any([True for i in read_db(db_file_name) if i["id"] == message.from_user.id and i["state"] == "wait team4"]))
async def hello_world(message):
    data_base = read_db(db_file_name)
    for i in data_base:
        if i["id"] == message.from_user.id:
            if str(message.text) in teams:
                await message.answer(match_results(teams_url_results[message.text]), reply_markup=button_start)
                i["state"] = ""
            else:
                await message.answer("try again")
    write_db(db_file_name, data_base)


#------------------------------------------------------------------------------------
    

@router.message(F.text == "started matches")
async def hello_world(message):
    await message.answer(started_matches(), reply_markup=button_start)


#------------------------------------------------------------------------------------


@router.message(F.text == "exit")
async def hello_world(message):
    await message.answer("ok", reply_markup=button_start)
    

#------------------------------------------------------------------------------------
