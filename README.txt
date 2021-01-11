Wechat Dictionary

Introduction

This project provide an "English to Chinese" dictionary lookup services to Wechat users via a Wechat public account.
It allows an user to send a English word to a Wechat Public Account and then get the corresponding Chinese translation
in return.

Comparing to other means of dictionary lookup service with a smart phone, this competitive advantage of this project is
convenience.  Here are the reasons.

First of all, starting Wechat is fast. Wechat is an essential communication application in the Chinese speaking community.
There are 1.17 billion Wechat users as of 2021-1-11, and there are over one billion daily active users of Wechat as of
early 2019. The active users to total users ratio shows that most Wechat users has Wechat running in the background all
the time. Therefore. starting Wechat is mostly just switching Wechat to the foreground, and this process should not take
too long.

Secondly, this project only needs minimal overhead of installation for Wechat users. In fact, there is no need for user
to install anything. Wechat is a platform application that has already provided all functionalities related to sending
text to and receiving text from a server. All users needed to do is to subscribe to a Wechat Public Account. It can be
as simple as scanning a QR code.

Lastly, the loading wait time is very short. There are only three steps required to lookup a word. They are starting
Wechat (very likely to be in the background already), find the public account (which can be pinned to the top of the
chat list for frequent users), and type the word. Compared to other means of dictionary lookup like via a webpage
(requiring loading a browser and a webpage) or a native app ( requiring loading the app itself and some possible
advertisements), the loading time of our project is trivial.

With the aforementioned reasons, I believe this project has its own niche market among the Chinese English users
( students and professionals).

Project Setup
This project has two components.
* Dictionary Preparation - fetching a dictionary from youdao.com and output a dictionary in the form of a python dict.
* Wechat Public Account Service - provide dictionary lookup services to users.

