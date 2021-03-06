'''regressionTest's server.
'''

__author__ = 'Simonas Joris'
__copyright__ = 'Copyright 2013, CERN CMS'
__credits__ = ['Giacomo Govi', 'Simonas Joris', 'Miguel Ojeda', 'Andreas Pfeiffer']
__license__ = 'Unknown'
__maintainer__ = 'Miguel Ojeda'
__email__ = 'mojedasa@cern.ch'


import cherrypy

import service
import html

import dataAccess


class Server(object):

    def ShowTable(self, curs):
        res1 = dataAccess.GetRunResults(curs[0])
        res2 = dataAccess.GetResultsList(res1[0][0])

        ret = '''
            <table id="header" bgcolor="#D8D8D8">
                <tr>
                    <td colspan = "2">Test Sequence:
                    <b>%s</b>&nbsp&nbsp&nbsp&nbsp
                    RunID:
                    %s&nbsp&nbsp&nbsp&nbsp
                    Time:
                    %s
                    </td>
                <tr>
                    <td>
                    Candidate:
                    <b>%s</b>&nbsp&nbsp&nbsp&nbsp
                    Architecture:
                    <b>%s</b>
                    </td>
                    <td class="links"><a href="showLogs?runID=%s">&gt&gt Logfile</a></td>
                </tr>
            </table>
            <table id="status">
                <tr>
                    <!--<th rowspan="2" colspan = "2">Reference releases</th>-->
                    <th>Reference release</th>
                    <th>Reference architecture</th>
        ''' % (curs[2], curs[0], curs[1], curs[3], curs[4], curs[0])

        for i in range(0, len(res2)):
            ret += '<th>%s</th>' % res2[i][2]

        ret += '</tr>'

        for rows in res1:
            res2 = dataAccess.GetResultsList(rows[0])

            ret += '''
                <tr>
                    <td align="left" >%s</td>
                    <td>%s</td>
            ''' % (rows[1], rows[2])

            for i in range(0, len(res2)):
                if res2[i][1] == 0:
                    ret += '<td align="center" bgcolor ="#A7C942"><b>OK</b></td>'
                else:
                    ret += '<td align="center" bgcolor ="#FF0000"><b>Failure</b></td>'

            ret += '</tr></tr>'

        ret += '</table><hr></body></html>'

        return ret

    @cherrypy.expose
    def index(self, release = '', arch = '', label = '', count = 2):

        labels = dataAccess.GetLabels()
        if not label:
            label = labels[0]

        count = int(count)
        if count > 100:
            count = 100
       
        ret = '''
        <html>
            <META HTTP-EQUIV="REFRESH" CONTENT="60">
            <head>
                <style type="text/css">
                    button,
                    input,
                    select,
                    textarea {
                      font-size: 100%;
                      margin: 0;
                      vertical-align: baseline;
                      *vertical-align: middle;
                    }
                    button, input {
                      line-height: normal;
                      *overflow: visible;
                    }
                    button::-moz-focus-inner, input::-moz-focus-inner {
                      border: 0;
                      padding: 0;
                    }
                    select {
                    }
                    button,
                    input[type="submit"] {
                      cursor: pointer;
                      -webkit-appearance: button;
                    }
                    input[type="search"] {
                      -webkit-appearance: textfield;
                      -webkit-box-sizing: content-box;
                      -moz-box-sizing: content-box;
                      box-sizing: content-box;
                    }
                    a {
                      color: #bfbfbf;
                      text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);
                      text-decoration:none;
                    }
                    a:hover, .active a {
                      color: #ffffff;
                      text-decoration: none;
                    }
                    .links {
                      background-color: #222;
                      background-color: #222222;
                      background-repeat: repeat-x;
                      background-image: -khtml-gradient(linear, left top, left bottom, from(#333333), to(#222222));
                      background-image: -moz-linear-gradient(top, #333333, #222222);
                      background-image: -ms-linear-gradient(top, #333333, #222222);
                      background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #333333), color-stop(100%, #222222));
                      background-image: -webkit-linear-gradient(top, #333333, #222222);
                      background-image: -o-linear-gradient(top, #333333, #222222);
                      background-image: linear-gradient(top, #333333, #222222);
                      filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#333333', endColorstr='#222222', GradientType=0);
                      -webkit-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25), inset 0 -1px 0 rgba(0, 0, 0, 0.1);
                      -moz-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25), inset 0 -1px 0 rgba(0, 0, 0, 0.1);
                      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25), inset 0 -1px 0 rgba(0, 0, 0, 0.1);
                    }
                    #status, #header
                    {
                        font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
                        width:100%;
                        border-collapse:collapse;
                    }
                    #header td 
                    {
                        font-size:1em;
                        border:1px solid #67645B;
                        padding:3px 7px 2px 7px;
                        text-align:left;
                    }
                    #status td
                    {
                        font-size:1em;
                        border:1px solid #67645B;
                        padding:3px 7px 2px 7px;
                    }
                    #status th 
                    {
                        border:1px solid #67645B;
                        font-size:1.1em;
                        text-align:center;
                        padding-top:5px;
                        padding-bottom:4px;
                        background-color:#ECAE12;
                        color:#ffffff;
                    }
                    #controls
                    {
                        font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
                        width:100%;
                        border-collapse:collapse;
                    }
                    #controls td 
                    {
                        font-size:1.1em;
                        border:none;
                        padding-top:5px;
                        padding-bottom:4px;
                        text-align:left;
                        background-color:#393333;
                        color:#ffffff;
                        
                    }
                    .topbar {
                      height: 40px;
                      position: fixed;
                      top: 0;
                      left: 0;
                      right: 0;
                      z-index: 10000;
                      overflow: visible;
                      color: #ffffff;
                      width: 100%;
                    }
                    .topbar form {
                      float: left;
                      margin: 5px 0 0 0;
                      position: relative;
                      filter: alpha(opacity=100);
                      -khtml-opacity: 1;
                      -moz-opacity: 1;
                      opacity: 1;
                    }
                    .topbar input {
                      background-color: #444;
                      background-color: rgba(255, 255, 255, 0.3);
                      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                      font-size: 80%;
                      font-weight: 13px;
                      line-height: 1;
                      padding: 4px 9px;
                      color: #fff;
                      color: rgba(255, 255, 255, 0.75);
                      border: 1px solid #111;
                      -webkit-border-radius: 4px;
                      -moz-border-radius: 4px;
                      border-radius: 4px;
                      -webkit-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1), 0 1px 0px rgba(255, 255, 255, 0.25);
                      -moz-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1), 0 1px 0px rgba(255, 255, 255, 0.25);
                      box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1), 0 1px 0px rgba(255, 255, 255, 0.25);
                      -webkit-transition: none;
                      -moz-transition: none;
                      transition: none;
                    }
                    .topbar input:-moz-placeholder {
                      color: #e6e6e6;
                    }
                    .topbar input::-webkit-input-placeholder {
                      color: #e6e6e6;
                    }
                    .topbar input:hover {
                      background-color: #bfbfbf;
                      background-color: rgba(255, 255, 255, 0.5);
                      color: #fff;
                    }
                    .topbar input:focus, .topbar input.focused {
                      outline: none;
                      background-color: #fff;
                      color: #404040;
                      text-shadow: 0 1px 0 #fff;
                      border: 0;
                      padding: 5px 10px;
                      -webkit-box-shadow: 0 0 3px rgba(0, 0, 0, 0.15);
                      -moz-box-shadow: 0 0 3px rgba(0, 0, 0, 0.15);
                      box-shadow: 0 0 3px rgba(0, 0, 0, 0.15);
                    }
                    .topbar-inner, .topbar .fill {
                      background-color: #222;
                      background-color: #222222;
                      background-repeat: repeat-x;
                      background-image: -khtml-gradient(linear, left top, left bottom, from(#333333), to(#222222));
                      background-image: -moz-linear-gradient(top, #333333, #222222);
                      background-image: -ms-linear-gradient(top, #333333, #222222);
                      background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #333333), color-stop(100%, #222222));
                      background-image: -webkit-linear-gradient(top, #333333, #222222);
                      background-image: -o-linear-gradient(top, #333333, #222222);
                      background-image: linear-gradient(top, #333333, #222222);
                      filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#333333', endColorstr='#222222', GradientType=0);
                      -webkit-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25), inset 0 -1px 0 rgba(0, 0, 0, 0.1);
                      -moz-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25), inset 0 -1px 0 rgba(0, 0, 0, 0.1);
                      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25), inset 0 -1px 0 rgba(0, 0, 0, 0.1);
                    }
                    .buts {
                    float: right;
                    }
                </style>
            </head>
            <body>
                <form method="get" action="index" >
                    <div class="topbar">
                        <div class="fill">
                            <div class="container">
                                <select name="label">
        '''

        for l in labels:
            ret += '<option value="%s" %s>%s</option>' % (l, 'selected="selected"' if label == l else '', l)

        ret += '''
                                </select>
                                Candidate Release: <input type="text" name="release" size="30" maxlength="50" %s />
                                Candidate Architecture: <input type="text" name="arch" size="15" maxlength="30" %s />
                                Number of results: <input type="text" name="count" size="1" maxlength="4" value="%s" />

                                <div class="buts">
                                    <input type="submit" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <br>
                </form>
        ''' % (
            ('value="%s"' % html.escape(release)) if release else '',
            ('value="%s"' % html.escape(arch)) if arch else '',
            count,
        )

        DBdata = dataAccess.GetReleasesHeaders(label, release, arch, count)

        if len(DBdata) == 0:
            ret += '<h3>No entries found</h3>'
        else:
            for data in DBdata:
                ret += self.ShowTable(data)

        return ret


    @cherrypy.expose
    def showLogs(self, runID):
        return '''
            <html>
                <head></head>
                <body>
                    <pre>%s</pre>
                </body>
            </html>
        ''' % dataAccess.GetReadLogStatus(int(runID))


def main():
    service.start(Server())


if __name__ == '__main__':
    main()

