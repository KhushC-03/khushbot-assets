import base64
import json
import random
import re
import requests
import ast
from flask import Flask, request, jsonify, render_template_string, session, make_response, redirect
from flask_login import login_user, LoginManager
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import threading
import time
app = Flask(__name__)




apikey = os.environ.get('apikey')
password = os.environ.get('password')
uri = os.environ.get('DATABASE_URL')
ENTRYKEY = os.environ.get('entryKey')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)






app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)
engine = create_engine(uri)








LETTERS = ['A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', 'K','L', 'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0','1','2','3','4','5','6','7','8','9','10']



def SIGNUPHTML():
    return """<!DOCTYPE html>
        <meta  name='viewport' content='width=device-width, initial-scale=0.8, shrink-to-fit=yes'>
        <body style="background-color:#1d1f33" ></body>


        <html>
            <style>
                html{
                    font-family: 'Rubik', sans-serif;
                }
                div{
                    position: relative;
                    top: 150px;
                    text-align: center;
                }
                h1{
                    text-align: center;
                    color: white;
                    font-size:1.5em;
                    position: relative;
                    top: 150px;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    white-space: nowrap;
                }
                h2{
                    text-align: center;
                    color: red;
                    font-size:1.5em;
                    position: relative;
                    top: 180px;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    white-space: nowrap;
                }
                label{
                    color: white;
                    font-size:1.3em;
                    
                }
                input{
                    font-size: 1.2em;
                    width: 450px;
                    height: 50px;
                    border-radius: 5px;
                    border:80px;
                    box-shadow: 0px 0px 2px 2px #3b3d71;
                    border-color: #3b3d71;
                    color: white;
                    background-color:#333563;
                    text-align: center;
                    margin-top:10px;
                    margin-bottom: 20px;
                }
            </style>
            <title>Sign up</title>
            <h1>Create your Khush Bot account.</h1>
            <h2>{{SIGNUPERROR}}</h2>
            <div>
                <form action='/signup' method='post'>
                    <br>
                    <label style='margin-left:-395px'>Email</label>
                    <br>
                    <input id='email' type='email' name='email' value='' >
                    <br>
                    <label style='margin-left:-360px'>Entry key</label>
                    <br>
                    <input id='password' type='password' name='password' value="">
                    <br>
                    <input type='submit' name='signup' style='background-color:royalblue; box-shadow: 0px 0px 1px 1px #3b3d71;'value='Create account'>
                    <br>
                    <label style='font-size:1em' onclick='signup()'>Click here to sign in</label>
                    <br>
                </form>
            </div>

        </html>

        <script type="text/javascript">
            function signup() {window.location.assign('https://khush-bot-key-management.herokuapp.com/signin')}
        </script>"""

def SIGNINHTML():
    return """
        <!DOCTYPE html>
        <meta  name='viewport' content='width=device-width, initial-scale=0.8, shrink-to-fit=yes'>
        <body style="background-color:#1d1f33" ></body>


        <html>
            <style>
                html{
                    font-family: 'Rubik', sans-serif;
                }
                div{
                    position: relative;
                    top: 150px;
                    text-align: center;
                }
                h1{
                    text-align: center;
                    color: white;
                    font-size:1.5em;
                    position: relative;
                    top: 150px;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    white-space: nowrap;
                }
                h2{
                    text-align: center;
                    color: red;
                    font-size:1.5em;
                    position: relative;
                    top: 180px;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    white-space: nowrap;
                }
                label{
                    color: white;
                    font-size:1.3em;
                    
                }
                input{
                    font-size: 1.2em;
                    width: 450px;
                    height: 50px;
                    border-radius: 5px;
                    border:80px;
                    box-shadow: 0px 0px 2px 2px #3b3d71;
                    border-color: #3b3d71;
                    color: white;
                    background-color:#333563;
                    text-align: center;
                    margin-top:10px;
                    margin-bottom: 20px;
                }
            </style>
            <title>Sign in</title>
            <h1>Sign in to your Khush Bot account.</h1>
            <h2>{{SIGNINERROR}}</h2>
            <div>
                <form action='/signin' method='post'>
                    <br>
                    <label style='margin-left:-395px'>Email</label>
                    <br>
                    <input id='email' type='email' name='email' value='' >
                    <br>
                    <label style='margin-left:-340px'>Licence Key</label>
                    <br>
                    <input id='licence' type='licence' name='licence' value="">
                    <br>
                    <input type='submit' name='signup' style='background-color:royalblue; box-shadow: 0px 0px 1px 1px #3b3d71;'value='Sign in'>
                    <br>
                    <label style='font-size:1em' onclick='signup()'>Click here to sign up</label>
                    <br>
                </form>
            </div>

        </html>

        <script type="text/javascript">
            function signup() {window.location.assign('https://khush-bot-key-management.herokuapp.com/signup')}
        </script>"""

def DASHHTML():
    return """<!DOCTYPE html>
        <meta  name='viewport' content='width=device-width, initial-scale=0.8, shrink-to-fit=yes'>
        <body style="background-color:#1d1f33" ></body>


        <html>
            <style>
                html{ 
                    font-family: 'Rubik', sans-serif;
                }
                div{
                    position: relative;
                    top: 60px;
                    text-align: center;
                }
                h1{
                    text-align: center;
                    color: white;
                    font-size:1.5em;
                    position: relative;
                    top: 60px;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    white-space: nowrap;
                }
                h2{
                    text-align: center;
                    color: rgb(255, 0, 0);
                    font-size:1.5em;
                    position: relative;
                    top: 90px;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    white-space: nowrap;
                }
                label{
                    color: white;
                    font-size:1.2em;
                    
                }
                input{
                    font-size: 1.2em;
                    width: 450px;
                    height: 50px;
                    border-radius: 5px;
                    border:80px;
                    box-shadow: 0px 0px 2px 2px #3b3d71;
                    border-color: #3b3d71;
                    color: white;
                    background-color:#333563;
                    text-align: center;
                    margin-top:10px;
                    margin-bottom: 20px;
                }
                .half-buttons{
                    width:225px;
                }
                .qtTitle{
                    font-size: 1.5em;   
                    color: white;
                    word-wrap: break-word;
                }
                .qtinfo{
                    word-wrap: break-word;
                    font-size: 1.5em;
                    color: white;
                }
                input:disabled {
                    color: #ffffff, -100%;
                }
                input:disabled {
                    color: #ffffff,  brightness(20000%);
                }
            </style>
            <title>Dashboard</title>
            <h1>Khush Bot Dashboard</h1>
            <h2></h2>
            <div>
                <br>
                <label style='margin-left:-395px'>Email</label>
                <br>
                <input id='email' type='email' name='email' value='{{EMAIL}}' disabled>
                <br>
                <label style='margin-left:-220px' onclick='showkey()'>Licence Key (click to show)</label> 
                <br>
                <input id='licence' type='password' name='licence' value="{{LICENCE}}" disabled>
                <br>
                <input type='submit' name='unbind' id='unbind' style='background-color:royalblue; box-shadow: 0px 0px 1px 1px #3b3d71;'value='{{MACHINESTATUS}}' onclick='unbind()'>
                <br>
                <input type='submit' class='half-buttons' name='download' style='background-color:royalblue; box-shadow: 0px 0px 1px 1px #3b3d71;'value='Download' onclick="download()">
                <input type='submit' class='half-buttons' name='statistics' style='background-color:royalblue; box-shadow: 0px 0px 1px 1px #3b3d71;'value='Statistics' onclick="statistics()">
                <br>
                <input type='submit' name='logout' style='background-color:rgb(225, 65, 65); box-shadow: 0px 0px 1px 1px #3b3d71;'value='Logout' onclick="logout()">
                <br>
                <label class='qtTitle' onclick=></label> 
                <br>
                <br>
                <label class='qtinfo' onclick=></label> 
                <br>
                <br>
            </div>

        </html>

        <script>
            function unbind(){
                var key = document.getElementById('licence').value;
                fetch(`https://khush-bot-key-management.herokuapp.com/unbindmachine?key=${key}`, {method: 'GET',})
                .then(response => response.json())
                .then(data => {
                    if (data.status == 'success'){
                        document.getElementById('unbind').value = 'Machine Unbound'
                    }
                });
        
            }
            function statistics(){
                window.location.assign("https://khush-bot-key-management.herokuapp.com/statistics")
            }
            function logout(){
                window.location.assign("https://khush-bot-key-management.herokuapp.com/logout")
                
            }
            function download() {
                window.open('{{DOWNLOAD}}')
            }
            function sleep (time) {
                return new Promise((resolve) => setTimeout(resolve, time));
            }
            function showkey(){
                if( document.getElementById('licence').type == 'text'){
                    document.getElementById('licence').type = 'password'
                }
                else{
                    document.getElementById('licence').type = 'text'
                }
                
            }
            if (window.location.href.includes('store')){
                var key = document.getElementById('licence').value;
                var store = window.location.href.split('store=')[1].split('&')[0].toUpperCase()
                var identifier = window.location.href.split('identifier=')[1]
                var quicktaskURL = `https://khush-bot-key-management.herokuapp.com/initqt?key=${key}&store=${store}&identifier=${identifier}`
                fetch(quicktaskURL, {method: 'GET',})
                .then(response => response.json())
                .then(data => 
                    {
                    if (data.status == 'success'){
                        document.querySelector('.qtTitle').innerHTML = 'Quick Task Started'
                        document.querySelector('.qtinfo').innerHTML = `Quick Task Identifier: ${identifier}`
                        sleep(4000).then(() => {
                            window.location.assign("https://khush-bot-key-management.herokuapp.com/dashboard")
                        });
                    }
                    else{
                        document.querySelector('.qtTitle').style = "color:rgb(255, 0, 0)"
                        document.querySelector('.qtTitle').innerHTML = data.message
                        document.querySelector('.qtinfo').style = "color:rgb(255, 0, 0)"
                        document.querySelector('.qtinfo').innerHTML = `Quick Task Identifier: ${identifier}`
                        sleep(4000).then(() => {
                            window.location.assign("https://khush-bot-key-management.herokuapp.com/dashboard")
                        });
                    }
                })
        
            }

        </script>
"""

def STATISTICSHTML():
    return """<!DOCTYPE html>
        <meta  name='viewport' content='width=device-width, initial-scale=0.8, shrink-to-fit=yes'>
        <body style="background-color:#1d1f33" ></body>


        <html>
            <style>
                html{
                    font-family: 'Rubik', sans-serif;
                }
                div{
                    position: relative;
                    top: 40px;
                    text-align: center;
                }
                h1{
                    text-align: center;
                    color: white;
                    font-size:1.5em;
                    position: relative;
                    top: 60px;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    white-space: nowrap;
                }
                h2{
                    text-align: center;
                    color: white;
                    font-size:1.5em;
                    position: relative;
                    top: 100px;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    white-space: nowrap;
                }
                .wrapper {
                    position: relative;
                    width: 400px;
                    height: 400px;
                    margin: auto;
                    flex-direction: row;
                }
                
                .container {
                    font-family: 'Rubik', sans-serif;
                }    
            </style>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <title>Statistics</title>
            <h1>Khush Bot Statistics</h1>
            <h2>Successful Checkouts</h2>
            <br>
            <div class="wrapper"> 
                <div class="container chart" data-size="400" data-value="{{CHECKOUTS}}" data-arrow="up">
            </div>
        </html>


        <script type="text/javascript">
            var Dial = function(container) {
                this.container = container;
                this.size = this.container.dataset.size;
                this.strokeWidth = this.size / 8;
                this.radius = (this.size / 2) - (this.strokeWidth / 2);
                this.value = this.container.dataset.value;
                this.direction = this.container.dataset.arrow;
                this.svg;
                this.defs;
                this.slice;
                this.overlay;
                this.text;
                this.arrow;
                this.create();
            }

            Dial.prototype.create = function() {
                this.createSvg();
                this.createDefs();
                this.createSlice();
                this.createOverlay();
                this.createText();
                this.createArrow();
                this.container.appendChild(this.svg);
            };

            Dial.prototype.createSvg = function() {
                var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                svg.setAttribute('width', this.size + 'px');
                svg.setAttribute('height', this.size + 'px');
                this.svg = svg;
            };

            Dial.prototype.createDefs = function() {
                var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
                var linearGradient = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
                linearGradient.setAttribute('id', 'gradient');
                var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
                stop1.setAttribute('stop-color', '#6E4AE2');
                stop1.setAttribute('offset', '0');
                linearGradient.appendChild(stop1);
                var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
                stop2.setAttribute('stop-color', '#78F8EC');
                stop2.setAttribute('offset', '{{LIMIT}}%');
                linearGradient.appendChild(stop2);
                var linearGradientBackground = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
                linearGradientBackground.setAttribute('id', 'gradient-background');
                var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
                stop1.setAttribute('stop-color', 'rgba(0, 0, 0, 0.2)');
                stop1.setAttribute('offset', '0');
                linearGradientBackground.appendChild(stop1);
                var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
                stop2.setAttribute('stop-color', 'rgba(0, 0, 0, 0.05)');
                stop2.setAttribute('offset', '{{LIMIT}}%');
                linearGradientBackground.appendChild(stop2);
                defs.appendChild(linearGradient);
                defs.appendChild(linearGradientBackground);
                this.svg.appendChild(defs);
                this.defs = defs;
            };

            Dial.prototype.createSlice = function() {
                var slice = document.createElementNS("http://www.w3.org/2000/svg", "path");
                slice.setAttribute('fill', 'none');
                slice.setAttribute('stroke', 'url(#gradient)');
                slice.setAttribute('stroke-width', this.strokeWidth);
                slice.setAttribute('transform', 'translate(' + this.strokeWidth / 2 + ',' + this.strokeWidth / 2 + ')');
                slice.setAttribute('class', 'animate-draw');
                this.svg.appendChild(slice);
                this.slice = slice;
            };

            Dial.prototype.createOverlay = function() {
                var r = this.size - (this.size / 2) - this.strokeWidth / 2;
                var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
                circle.setAttribute('cx', this.size / 2);
                circle.setAttribute('cy', this.size / 2);
                circle.setAttribute('r', r);
                circle.setAttribute('fill', 'url(#gradient-background)');
                this.svg.appendChild(circle);
                this.overlay = circle;
            };

            Dial.prototype.createText = function() {
                var fontSize = this.size / 3.5;
                var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                text.setAttribute('x', (this.size / 2) + fontSize / 7.5);
                text.setAttribute('y', (this.size / 2) + fontSize / 4);
                text.setAttribute('font-family', 'Century Gothic, Lato');
                text.setAttribute('font-size', fontSize);
                text.setAttribute('fill', '#78F8EC');
                text.setAttribute('text-anchor', 'middle');
                var tspanSize = fontSize / 3;
                text.innerHTML = 0 + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">&nbsp;&nbsp;&nbsp;</tspan>';
                this.svg.appendChild(text);
                this.text = text;
            };

            Dial.prototype.createArrow = function() {
                var arrowSize = this.size / 10;
                var arrowYOffset, m;
                if(this.direction === 'up') {
                    arrowYOffset = arrowSize / 2;
                    m = -1;
                }
                else if(this.direction === 'down') {
                    arrowYOffset = 0;
                    m = 1;
                }
                var arrowPosX = ((this.size / 2) - arrowSize / 2);
                var arrowPosY = (this.size - this.size / 3) + arrowYOffset;
                var arrowDOffset =  m * (arrowSize / 1.5);
                var arrow = document.createElementNS("http://www.w3.org/2000/svg", "path");
                arrow.setAttribute('d', 'M 0 0 ' + arrowSize + ' 0 ' + arrowSize / 2 + ' ' + arrowDOffset + ' 0 0 Z');
                arrow.setAttribute('fill', '#97F8F0');
                arrow.setAttribute('opacity', '0.6');
                arrow.setAttribute('transform', 'translate(' + arrowPosX + ',' + arrowPosY + ')');
                this.svg.appendChild(arrow);
                this.arrow = arrow;
            };

            Dial.prototype.animateStart = function() {
                var v = 0;
                var self = this;
                var intervalOne = setInterval(function() {
                    var p = +(v / self.value).toFixed(2);
                    var a = (p < 0.95) ? 2 - (2 * p) : 0.05;
                    v += a;
                    if(v >= +self.value) {
                        v = self.value;
                        clearInterval(intervalOne);
                    }
                    self.setValue(v);
                }, 10);
            };

            Dial.prototype.animateReset = function() {
                this.setValue(0);
            };

            Dial.prototype.polarToCartesian = function(centerX, centerY, radius, angleInDegrees) {
            var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;
            return {
                x: centerX + (radius * Math.cos(angleInRadians)),
                y: centerY + (radius * Math.sin(angleInRadians))
            };
            }

            Dial.prototype.describeArc = function(x, y, radius, startAngle, endAngle){
                var start = this.polarToCartesian(x, y, radius, endAngle);
                var end = this.polarToCartesian(x, y, radius, startAngle);
                var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
                var d = [
                    "M", start.x, start.y, 
                    "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
                ].join(" ");
                return d;       
            }

            Dial.prototype.setValue = function(value) {	
                    var c = (value / {{LIMIT}}) * 360;
                    if(c === 360)
                        c = 359.99;
                    var xy = this.size / 2 - this.strokeWidth / 2;
                    var d = this.describeArc(xy, xy, xy, 180, 180 + c);
                this.slice.setAttribute('d', d);
                var tspanSize = (this.size / 3.5) / 3;
                this.text.innerHTML = Math.floor(value) + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">&nbsp;&nbsp;&nbsp;</tspan>';
            };

            var containers = document.getElementsByClassName("chart");
            var dial = new Dial(containers[0]);
            dial.animateStart();
        </script>"""

def HOMEPAGE():
    return """
        <!DOCTYPE html>
        <meta  name='viewport' content='width=device-width, initial-scale=0.8, shrink-to-fit=yes'>
        <body style="background-color:#1d1f33" ></body>
        <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
        <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>

        <style>
            @font-face { font-family: Harabara; src: url('https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/madani-medium.ttf'); }
            html{
                font-family: Harabara;
                scroll-behavior: smooth;
                letter-spacing:0.07em;
                
            }
            .div{
                position: relative;
                text-align: center;
            }

            .dashbutton{
                position: relative;
                margin-top:20px;
                margin-left:10px;
                width:140px;
                height:45px;
                background: #3a4fc6;
                border-radius:10px;
                padding-top:22px;
                text-align: center;
                -webkit-box-shadow:0 0 5px #3a4fc6; 
                -moz-box-shadow: 0 0 5px #3a4fc6; 
                box-shadow:0 0 5px #3a4fc6;
            }
            .dashlabel{
                
                font-size:20px;
                color: white;
            }
            h1{
                text-align: center;
                color: white;
                font-size:2.6em;
                position: relative;
                top: 80px;
                white-space: nowrap;
                

            }

            h2{
                position: relative;
                text-align: center;
                color: white;
                font-size: 2em;
                word-wrap: break-word;

            }
            .sub1{
                top: 90px;
                position: relative;
                text-align: center;
                margin: 0 auto;
                width: 85vw;
                max-width: 900px;
                word-wrap: break-word;

            }


            .cliImage{

                text-align: center;
                position: relative;
                top: 150px;
                width: 92vw;
                max-width: 1000px;
                

                
            }
            .cli{
                text-align: center;
                margin: 0 auto;
            }
            .sold-out{
                text-align: center;
                position: relative;
                top:210px;
                background-color:#3a4fc6;
                height: 50px;
                margin: 0 auto;
                width: 280px;
                border: none !important;
                border-radius:10px;
                padding-top: 25px;
                -webkit-box-shadow:0 0 5px #3a4fc6; 
                -moz-box-shadow: 0 0 5px #3a4fc6; 
                box-shadow:0 0 5px #3a4fc6;
            }
            .oostext{
                font-size: 1.4em;
                text-align: center;
                color: white;
            }

            .scroll-container{
                top:300px;
                text-align: center;
                position: relative;
                margin: 0 auto;
                overflow: auto;
                white-space: nowrap;
                padding-left: 7.5px;
                padding-right: 7.5px;
                padding-top:7.5px;
                padding-bottom: 7.5px;
                background: #181a2b;
                height: auto;
                max-width: 900px;
                border-radius:20px;
                -ms-overflow-style: none;
                scrollbar-width: none;
                overscroll-behavior: contain;
            }
            .scroll-container::-webkit-scrollbar {
                display: none;
            }  
            .gridscroll{
                display:inline-block;
            }
            
            .gridscroll img {
                margin-right:22px;
                height:160px;
                border-radius:20px;
                width: auto;
                background-color:#181a2b;
                
            }

            .allfeatures{
                top:350px;
                position: relative;
                width: auto;
                height: 305px;
                max-width: 900px;
                max-height: 485px;
                
                text-align: left;
                margin: 0 auto;
                background-color: #181a2b;
                border-radius:20px;
                padding-top: 20px;
                padding-bottom: 20px;
            }
            .container {
                display: flex;
                align-items: center;
                padding-bottom:30px
        
            }

            .feature-image1 {
                width:60px;
                height:60px;
                background-color: #aaffc0;
                border-radius:10px;
                margin-left: 20px;
                padding: 5px 5px 5px 5px;
                border:none;
                -webkit-box-shadow:0 0 5px #aaffc0; 
                -moz-box-shadow: 0 0 5px #aaffc0; 
                box-shadow:0 0 5px #aaffc0;
            }

            .feature-image2 {
                width:60px;
                height:60px;
                background-color: #ffeea5;
                border-radius:10px;
                margin-left: 20px;
                padding: 5px 5px 5px 5px;
                border:none;
                -webkit-box-shadow:0 0 5px #ffeea5; 
                -moz-box-shadow: 0 0 5px #ffeea5; 
                box-shadow:0 0 5px #ffeea5;
            }

            .feature-image3 {
                text-align: center;
                width:60px;
                height:60px;
                background-color: #96e0f9;
                border-radius:10px;
                margin-left: 20px;
                padding: 5px 5px 5px 5px;
                border:none;
                -webkit-box-shadow:0 0 5px #96e0f9; 
                -moz-box-shadow: 0 0 5px #96e0f9; 
                box-shadow:0 0 5px #96e0f9;
            }
            .text {
                font-size: 1.3em;
                margin-left: 15px;
                margin-right: 4px;
                color:white;
                letter-spacing:0.08em;
            }

            .qt-italics{
                font-size:0.8em;
            }
            
            @media (max-width: 700px) {
                .scroll-container{
                    width:430px
                }
                .allfeatures{
                    width: 450px;
                }
            }
        </style>


        <html>
            <title>Khush Bot</title>

            <div  class="dashbutton" onclick='window.location.assign("https://khush-bot-key-management.herokuapp.com/dashboard")' data-aos="fade-down">
                <label class="dashlabel">Dashboard</label>
            </div>
            <div class="fixed-div">
                <h1 class="BeforeScroll">KhushBot</h1>
                <div class='subheader'>
                    <h2 class='sub1'>The all in one software solution allowing you to secure limited sneakers with ease.</h2>
                </div>
                
            </div>


            <div class="cli" data-aos="fade-left"> <img class='cliImage' src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/unknown.png"></div>

            <div class="sold-out" data-aos="fade-up">
                <span class='oostext'>OUT OF STOCK</span>
            </div> 
            <div class="storebox" >
                <div class="scroll-container" data-aos="fade-left">
                    <div class="gridscroll">
                    <img src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/footasylum.png" class='storeimages'>
                    <img src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/office.png" class='storeimages'>
                    <img src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/offspring.png" class='storeimages'>          
                    <img src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/asos.png" class='storeimages'>
                    <img src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/offwhite.png" class='storeimages'>
                    <img src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/wellgosh.png" class='storeimages'>
                    </div>
                </div>
            </div>
            <br><br>
            <div class='allfeatures' data-aos="fade-right">
                <div class="container">
                    <div class="image">
                    <img class="feature-image1" src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/worldwide.png">
                    </div>
                    <div class="text">
                    <label>Quicktasks allow you to remotely start tasks from anywhere in the world.</label>
                </div>
                
            </div>
            <div class="container" >
                <div class="image">
                <img class="feature-image2" src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/ai.png">
                </div>
                <div class="text text2">
                <label>Intelligent anti-bot solving algorithms.</label>
                </div>
        
            </div>
            <div class="container">
                <div class="image">
                    <img class="feature-image3" src="https://raw.githubusercontent.com/KhushC-03/khushbot-assets/main/settings.png">
                </div>
                <div class="text">
                    <label>Mass change capabilities, giving you full control of your bot.</label>
                </div>
            
                </div>

        </html>




        <script>
            window.scrollTo({ top: 0, behavior: 'smooth' });
            AOS.init({
                duration: 1200,
            })

        </script>
"""

def deleteQT(licenseKey):
    time.sleep(5)
    engine.execute(
        f"""
        UPDATE quicktask
        SET store = 'none', identifier = 'none', status = 'off'
        WHERE key = '{licenseKey}';
    """)

def randomKeygen():
    randomKey = []
    for i in range(3):
        random4th = []
        for i in range(5):
            if random.randint(1,2) == 1:
                random4th.append(random.choice(LETTERS))
            else:random4th.append(random.choice(NUMBERS))
        randomKey.append(''.join(random4th)) 
    return 'KB-'+'-'.join(randomKey)

@app.route('/home',methods=['GET', 'POST'])
def homepage():
    return render_template_string(HOMEPAGE())

@app.route('/',methods=['GET'])
def home():
    return redirect('signin'),302

@app.route('/checkouts',methods=['GET','POST'])
def addcheckout():
    if request.method == 'POST':
        key = request.form.get('key')
        initialCheckouts = engine.execute(f"""
            SELECT checkouts from keys
            WHERE key = '{key}';
            """  ).first()[0]
        updatedCheckout = int(initialCheckouts) + 1
        
        engine.execute(
            f"""
            UPDATE keys
            SET checkouts = '{updatedCheckout}'
            WHERE key = '{key}';
        """)   
        return jsonify({'status':'success','checkouts':updatedCheckout}), 200
    else:
        key = request.args.get('key')
        initialCheckouts = engine.execute(f"""
            SELECT checkouts from keys
            WHERE key = '{key}';
            """  ).first()[0]
        return jsonify({'status':'success','checkouts':initialCheckouts}), 200
 
 
@app.route('/purchases',methods=['GET','POST'])
def purchases():
    if request.method == 'POST':
        key = request.form.get('key')
        initialpurchases = engine.execute(f"""
            SELECT purchases from keys
            WHERE key = '{key}';
            """  ).first()[0] 
        if len(initialpurchases) == 0 or initialpurchases == 'none':
            jsonPurchases = {
                'product': request.form.get('product'),
                'price':request.form.get('price'),
                'site':request.form.get('site'),
                'image':request.form.get('image'),
                'identifier':request.form.get('identifier')
            }
            stringPurchases = f"[{json.dumps(jsonPurchases)}]"
            engine.execute(
                f"""
                UPDATE keys
                SET purchases = '{stringPurchases}'
                WHERE key = '{key}';
            """) 
            return jsonify({'status':'success','purchases':jsonPurchases})
        else:
            initialpurchases = engine.execute(f"""
                SELECT purchases from keys
                WHERE key = '{key}';
                """  ).first()[0]       
            purchases = ast.literal_eval(initialpurchases)
            purchases.append({
                'product': request.form.get('product'),
                'price':request.form.get('price'),
                'site':request.form.get('site'),
                'image':request.form.get('image'),
                'identifier':request.form.get('identifier')
            })  
            engine.execute(
                f"""
                UPDATE keys
                SET purchases = '{json.dumps(purchases)}'
                WHERE key = '{key}';
            """) 
            return jsonify({'status':'success','purchases':purchases})
    else:
        key = request.args.get('key')
        initialpurchases = engine.execute(f"""
                SELECT purchases from keys
                WHERE key = '{key}';
                """  ).first()[0]
        try:
            return jsonify({'status':'success','purchases':json.loads(initialpurchases)})
        except:
            return jsonify({'status':'success','purchases':initialpurchases})

@app.route('/unbindmachine',methods=['GET'])
def unbindmachine(): 
    key = request.args.get('key')
    engine.execute(
        f"""
        UPDATE keys
        SET machine = 'none'
        WHERE key = '{key}';
    """)       
    return jsonify({'status':'success','machine':'none'}),200

@app.route('/machine',methods=['GET','POST'])
def setmachine(): 
    if request.method == 'POST':
        key = request.form.get('key')
        machine = request.form.get('machine')
        engine.execute(
            f"""
            UPDATE keys
            SET machine = '{machine}'
            WHERE key = '{key}';
        """)       
        return jsonify({'status':'success','machine':machine}),200
    else:
        key = request.args.get('key')
        machine = engine.execute(f"""
            SELECT machine from keys
            WHERE key = '{key}';
            """  ).first()[0]   
        return jsonify({'status':'success','machine':machine}),200  

@app.route('/addKey',methods=['POST'])
def addkey():
    if request.form.get('password') == password:
        KEY = randomKeygen()
        while True:
            if KEY in [k[0] for k in engine.execute("""
                SELECT ALL key FROM keys;""").fetchall()]:
                KEY = randomKeygen()
            else:
                break        
        engine.execute(
            f"""
            INSERT INTO quicktask (store, identifier, key, status)
            VALUES ( 'none', 'none', '{KEY}', 'none');
        """)
        if len(request.form.get('Email')) > 0:
            email = base64.b64encode(request.form.get('Email').lower().encode()).decode() 
            
            engine.execute(
                f"""
                INSERT INTO keys (key, email, userinformation, machine, checkouts, purchases)
                VALUES ('{KEY}', '{email}', 'none', 'none', '0', 'none');
            """)
        else:
            engine.execute(
                f"""
                INSERT INTO keys (key, email, userinformation, machine, checkouts, purchases)
                VALUES ('{KEY}', 'none', 'none', 'none', '0', 'none');
            """)
        return jsonify({'status':'success',"message":'key added successfully','data':KEY}), 200  
    else:
        return jsonify({'status':'failure'}), 403 
 
@app.route('/checkkey',methods=['POST'])
def checkkey():
    if request.form.get('password') == password:
        if request.form.get('key') in [k[0] for k in engine.execute("""
            SELECT ALL key FROM keys;
            """).fetchall()]:
            return jsonify({'status':'success'}), 200  
        else:
            return jsonify({'status':'failure'}), 200  
        
    else:
        return jsonify({'status':'failure'}), 403 
    
@app.route('/initqt',methods=['GET'])
def initqt():
    if request.args.get('key') in [k[0] for k in engine.execute("""
        SELECT ALL key FROM keys;
        """).fetchall()]:
        store = request.args.get('store')
        if len(store) == 0:
            return jsonify({'status':'failure','message':'Store not provided'}), 400  
        identifier = request.args.get('identifier')
        if len(identifier) == 0:
            return jsonify({'status':'failure','message':'Identifier not provided'}), 400  
        key = request.args.get('key')
        engine.execute(
            f"""
            UPDATE quicktask
            SET store = '{store}', identifier = '{identifier}', status = 'active'
            WHERE key = '{key}';
        """)
        threading.Thread(target=deleteQT,args=(key,)).start()
        return jsonify({'status':'success'}), 200  
    else:
        return jsonify({'status':'failure','message':'Key not found'}), 400  
        
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'GET':
        return render_template_string(SIGNUPHTML()), 200
    else:
        if request.form.get('password') != ENTRYKEY:
            return render_template_string(SIGNUPHTML(),SIGNUPERROR='Entry key mis-match'), 400
        else:
            
            try:
                checkEmail = base64.b64encode(request.form.get('email').lower().encode()).decode()
                engine.execute(f"""
                SELECT key from keys
                WHERE email = '{checkEmail}';
                """  ).first()[0]
                return render_template_string(SIGNUPHTML(),SIGNUPERROR='Email already in use'), 400
            except:
                pass
            email = request.form.get('email').lower()
            r = requests.post('https://khush-bot-key-management.herokuapp.com/addKey',data={'password':'Khushchau050320','Email':email})    
            key = r.json()['data']  
            resp = make_response(redirect("/dashboard", code=302))
            sessionCookie = base64.urlsafe_b64encode(json.dumps({"key":key,"user":email,"expiry":time.time()+60*60*24*365}).encode()).decode()
            resp.set_cookie('session', sessionCookie,max_age=365 * 60 * 60 * 24)
            return resp

@app.route('/statistics',methods=['GET'])
def statistics():
    if request.cookies.get('session'):
        sessionCookie = json.loads(base64.b64decode(request.cookies.get('session')))
        key = sessionCookie['key']
        Checkouts = engine.execute(f"""
            SELECT checkouts from keys
            WHERE key = '{key}';
            """  ).first()[0]
        return render_template_string(STATISTICSHTML(),CHECKOUTS=Checkouts,LIMIT=int(Checkouts)+25)
    else:
        return redirect("/signin", code=302)   

@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method == 'GET':
        if request.cookies.get('session'):
            return redirect("/dashboard", code=302)
        else:
            return render_template_string(SIGNINHTML()), 200
    else:
        if len(request.form.get('email')) == 0:
            return render_template_string(SIGNINHTML(),SIGNINERROR="Email not provided"), 400
        if len(request.form.get('licence')) == 0:
            return render_template_string(SIGNINHTML(),SIGNINERROR="Licence Key not provided"), 200
        email = base64.b64encode(request.form.get('email').lower().encode()).decode()
        licence = request.form.get('licence')
        
        
        try:
            authresult = engine.execute(f"""
                SELECT key from keys
                WHERE email = '{email}';
                """  ).first()[0]
            if licence != authresult:
                return render_template_string(SIGNINHTML(),SIGNINERROR="Key not found"), 400
            else:
                resp = make_response(redirect("/dashboard", code=302))
                sessionCookie = base64.urlsafe_b64encode(json.dumps({"key":authresult,"user":request.form.get('email').lower(),"expiry":time.time()+60*60*24*365}).encode()).decode()
                resp.set_cookie('session', sessionCookie,max_age=365 * 60 * 60 * 24)
                return resp
        except Exception as e:
            return render_template_string(SIGNINHTML(),SIGNINERROR='Email cannot be found'), 400
  
@app.route('/logout',methods=['GET'])
def logout():
    if request.cookies.get('session'):
        resp = make_response(redirect("/signin", code=302))
        resp.delete_cookie('session')
        return resp    
    return 'cannot log out'        
  
@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    if request.cookies.get('session'):
        sessionCookie = json.loads(base64.b64decode(request.cookies.get('session')))
        if time.time() > sessionCookie['expiry']:
            return render_template_string(SIGNINHTML()), 400 
        email = sessionCookie['user']
        key = sessionCookie['key']
        if key in [k[0] for k in engine.execute("""
            SELECT ALL key FROM keys;
            """).fetchall()]:
            downloadURL = requests.get('https://khushc-03.github.io/scripts-Zm9vdGFzeWx1bWZyb250ZW5k/download.json').json()['url']
            machine = engine.execute(f"""
                SELECT machine from keys
                WHERE key = '{key}';
                """  ).first()[0] 
            if machine == 'none':
                machineStatus = 'Machine Unbound'
            else:
                machineStatus = 'Unbind Machine'  
            return render_template_string(DASHHTML(),EMAIL=email,LICENCE=key,DOWNLOAD=downloadURL,MACHINESTATUS=machineStatus), 200
        else:
            resp = make_response(redirect("/signin", code=302))
            resp.delete_cookie('session')
            return resp
    else:
       return redirect("/signin", code=302)


if __name__ == "__main__":
    app.run()
  

# http://127.0.0.1:5000/dashboard?store=wellgosh&identifier=bnjnjn



