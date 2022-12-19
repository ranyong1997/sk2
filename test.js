const CryptoJS = require("crypto-js");

const encrypt = function (e) {
    var f = CryptoJS.enc.Utf8.parse("learnspaceaes123");
    var d = CryptoJS.AES.encrypt(e, f, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return d.toString()
};

const decrypt = function (e) {
    var cipherParams = CryptoJS.lib.CipherParams.create({
        ciphertext: CryptoJS.enc.Base64.parse(e)
    });
    var f = CryptoJS.enc.Utf8.parse("learnspaceaes123");
    var res = CryptoJS.AES.decrypt(cipherParams, f, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return res.toString(CryptoJS.enc.Utf8);

}

const timeToSeconds = function (f) {
    var b = f.split(":");
    var d = parseInt(b[0]);
    var a = parseInt(b[1]);
    var c = parseInt(b[2]);
    var e = d * 3600 + a * 60 + c;
    return e
};

const formatStr = function (c, a) {
    var l = "";
    var k = (c + "").length;
    if (k > 0) {
        if (k + 2 > a) {
            return c + ""
        } else {
            var g = a - k - 2;
            var h = 1;
            for (var e = 0; e < g; e++) {
                h = h * 10
            }
            var b = parseInt(Math.random() * h);
            var f = (b + "").length;
            if (f < g) {
                for (var d = f; d < g; d++) {
                    b = b * 10
                }
            }
            if (k >= 10) {
                l += k
            } else {
                l += "0" + k
            }
            l += c + (b + "")
        }
    } else {
        return c + ""
    }
    return l
};

const getParams = function (p) {
    var q = {
        courseId: p.courseId,
        itemId: p.itemId,
        time1: formatStr(
            (new Date()).getTime(),
            20
        ),
        time2: formatStr(parseInt(p.startTime), 20),
        time3: formatStr(timeToSeconds(p.videoTotalTime), 20),
        time4: formatStr(parseInt(p.endTime), 20),
        videoIndex: p.videoIndex || 0,
        time5: formatStr(p.studyTimeLong, 20),
        terminalType: p.terminalType || 0
    };
    return q
}

var itemids = process.argv[2];
var start = process.argv[3]
var end = process.argv[4]
var p = {
    "interval": true,
    "playComplete": true,
    "courseId": "1754b2c1a83f4268a668e959b9d3941a___", // 代表当前学习课程的16进制id
    "itemId": itemids, // 应课程中的每个视频或者文档也有一个16进制id
    "position": 4,
    "videoTotalTime": "00:10:35",
    "startTime": parseInt(start),   // 对应时长进度
    "endTime": parseInt(end),   // 对应时长，表示当前视频从startTime秒学习到了endTime的秒数
    "studyTimeLong": end - start
}
console.log(encrypt(JSON.stringify(getParams(p))))