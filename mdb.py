#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex

import base64
import re
import pymongo

from pymongo.errors import DuplicateKeyError
from marshmallow.exceptions import ValidationError

from config import DATABASE_URI, DATABASE_NAME, CHANNEL_LINK, WEB_SITE_URL, SUB_TEXT, BOT_URL


myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

async def encode_iru(string):
    array_link_iru = string.split("/")
    numCutNum = array_link_iru[len(array_link_iru)-1]
    outEncStr = "get-"+numCutNum+"-irupc-get"
    string_bytes = outEncStr.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    base64_string_aslink = BOT_URL+base64_string
    return base64_string_aslink

async def savefiles(docs, group_id):
    mycol = mydb[str(group_id)]
    
    try:
        mycol.insert_many(docs, ordered=False)
    except Exception:
        pass


async def channelgroup(channel_id, channel_name, group_id, group_name):
    mycol = mydb["ALL DETAILS"]

    channel_details = {
        "channel_id" : channel_id,
        "channel_name" : channel_name
    }

    data = {
        '_id': group_id,
        'group_name' : group_name,
        'channel_details' : [channel_details],
    }
    
    if mycol.count_documents( {"_id": group_id} ) == 0:
        try:
            mycol.insert_one(data)
        except:
            print('Some error occured!')
        else:
            print(f"files in '{channel_name}' linked to '{group_name}' ")
    else:
        try:
            mycol.update_one({'_id': group_id},  {"$push": {"channel_details": channel_details}})
        except:
            print('Some error occured!')
        else:
            print(f"files in '{channel_name}' linked to '{group_name}' ")


async def ifexists(channel_id, group_id):
    mycol = mydb["ALL DETAILS"]

    query = mycol.count_documents( {"_id": group_id} )
    if query == 0:
        return False
    else:
        ids = mycol.find( {'_id': group_id} )
        channelids = []
        for id in ids:
            for chid in id['channel_details']:
                channelids.append(chid['channel_id'])

        if channel_id in channelids:
            return True
        else:
            return False


async def deletefiles(channel_id, channel_name, group_id, group_name):
    mycol1 = mydb["ALL DETAILS"]

    try:
        mycol1.update_one(
            {"_id": group_id},
            {"$pull" : { "channel_details" : {"channel_id":channel_id} } }
        )
    except:
        pass

    mycol2 = mydb[str(group_id)]
    query2 = {'channel_id' : channel_id}
    try:
        mycol2.delete_many(query2)
    except:
        print("Couldn't delete channel")
        return False
    else:
        print(f"filters from '{channel_name}' deleted in '{group_name}'")
        return True


async def deletealldetails(group_id):
    mycol = mydb["ALL DETAILS"]

    query = { "_id": group_id }
    try:
        mycol.delete_one(query)
    except:
        pass


async def deletegroupcol(group_id):
    mycol = mydb[str(group_id)]

    if mycol.count() == 0:
        return 1

    try:    
        mycol.drop()
    except Exception as e:
        print(f"delall group col drop error - {str(e)}")
        return 2
    else:
        return 0


async def channeldetails(group_id):
    mycol = mydb["ALL DETAILS"]

    query = mycol.count_documents( {"_id": group_id} )
    if query == 0:
        return False
    else:
        ids = mycol.find( {'_id': group_id} )
        chdetails = []
        for id in ids:
            for chid in id['channel_details']:
                chdetails.append(
                    str(chid['channel_name']) + " ( <code>" + str(chid['channel_id']) + "</code> )"
                )
            return chdetails


async def countfilters(group_id):
    mycol = mydb[str(group_id)]

    query = mycol.count()

    if query == 0:
        return False
    else:
        return query

        
async def findgroupid(channel_id):
    mycol = mydb["ALL DETAILS"]

    ids = mycol.find()
    groupids = []
    for id in ids:
        for chid in id['channel_details']:
            if channel_id == chid['channel_id']:
                groupids.append(id['_id'])
    return groupids

# Search Query for TG Files
async def searchquery(group_id, name):

    mycol = mydb[str(group_id)]

    filenames = []
    filelinks = []
    ##Start
    name = name.split(' tg')[0]
    ##End
    name = name.replace(" tg", "")
    
    # looking for a better regex :(
    pattern = name.lower().strip().replace(' ','.*')
    raw_pattern = r"\b{}\b".format(pattern)
    regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    
    query = mycol.find( {"file_name": regex} )
    indexValIru = 0
    for file in query:
        if file['file_size'] == "📺":
            filename = "📺"+ file['file_name']
            filelink = file['link']
            filenames.insert(indexValIru,filename)
            filelinks.insert(indexValIru,filelink.replace(" ", "."))
            indexValIru = indexValIru+1
        else:
            try:
              if file['file_name'].index(".srt")> 0:
                  filename = SUB_TEXT + file['file_name']
                  filelink = file['link']
            except:
                try:
                    if file['file_name'].index(".zip")> 0:
                        filename = SUB_TEXT + file['file_name']
                        filelink = file['link']
                except:
                    try:
                        if file['file_name'].index(".rar")> 0:
                            filename = SUB_TEXT + file['file_name']
                            filelink = file['link']
                    except:
                        fName_mod = ' '.join(word for word in file['file_name'].replace(".", " ").replace("-", " ").split(' ') if not word.startswith('@'))
                        filename = "[" + str(file['file_size']//1048576) + "MB] " + fName_mod
                        filelink = await encode_iru(file['link'])

            filenames.append(filename)
            filelinks.append(filelink)
    return filenames, filelinks

# Search Query for Subtitle
async def searchquery_sub(group_id, name):

    mycol = mydb[str(group_id)]

    filenames = []
    filelinks = []
    name = name.replace(" sub", "").replace("sub ", "").replace("sub", "")
    
    # looking for a better regex :(
    pattern = name.lower().strip().replace(' ','.*')
    raw_pattern = r"\b{}\b".format(pattern)
    regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    
    query = mycol.find( {"file_name": regex} )
    indexValIru = 0
    for file in query:
        if file['file_size'] != "📺":
            try:
              if file['file_name'].index("srt")> 0:
                  filename = SUB_TEXT + file['file_name']
                  filelink = file['link']
                  filenames.append(filename)
                  filelinks.append(filelink)
            except:
                try:
                    if file['file_name'].index("zip")> 0:
                        filename = SUB_TEXT + file['file_name']
                        filelink = file['link']
                        filenames.append(filename)
                        filelinks.append(filelink)
                except:
                    try:
                        if file['file_name'].index("rar")> 0:
                            filename = SUB_TEXT + file['file_name']
                            filelink = file['link']
                            filenames.append(filename)
                            filelinks.append(filelink)
                    except:
                        if file['file_name'] == "":
                            print("zero")
    return filenames, filelinks


# Search Query for Direct Links
async def searchquery_link(group_id, name):

    mycol = mydb[str(group_id)]

    filenames = []
    filelinks = []

    # looking for a better regex :(
    pattern = name.lower().strip().replace(' ','.*')
    raw_pattern = r"\b{}\b".format(pattern)
    regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    
    query = mycol.find( {"file_name": regex} )
    indexValIru = 0
    for file in query:
        if file['file_size'] == "📺":
            filename = file['file_name']
            filelink = file['link']
            filenames.insert(indexValIru,filename)
            filelinks.insert(indexValIru,filelink)
            indexValIru = indexValIru+1
        else:
            try:
              if file['file_name'].index(".srt")> 0:
                  filename = SUB_TEXT + file['file_name']
                  filelink = file['link']
            except:
                try:
                    if file['file_name'].index(".zip")> 0:
                        filename = SUB_TEXT + file['file_name']
                        filelink = file['link']
                except:
                    try:
                        if file['file_name'].index(".rar")> 0:
                            filename = SUB_TEXT + file['file_name']
                            filelink = file['link']
                    except:
                        fName_mod = ' '.join(word for word in file['file_name'].replace(".", " ").replace("-", " ").split(' ') if not word.startswith('@'))
                        filename = "[" + str(file['file_size']//1048576) + "MB] " + fName_mod
                        filelink = file['link']+"/"+fName_mod+"?size?"+str(file['file_size']//1048576) + "MB"

            filenames.append(filename)
            filelinks.append(filelink.replace(" ", ".").replace(CHANNEL_LINK, WEB_SITE_URL))
    return filenames, filelinks
