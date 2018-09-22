var fs = require('fs');

var print = s => (s + " ".repeat(20)).substr(0,20);

var r = [], x = {}, y={}, n=m=0;

var files = fs.readdirSync('./json'); 
files.forEach(file=>{
  // var body = JSON.parse(fs.readFileSync('./json/'+file,'utf8').replace(/, \"disc.+/,'}')); 
  var author = fs.readFileSync('./json/'+file,'utf8').match(/(?<=author\": \")(.*)(?=\", \"disc)/);
  // var lang = fs.readFileSync('./json/'+file,'utf8').match(/(?<=language\": \")(.*)(?=\")/);
  // var lang = fs.readFileSync('./json/'+file,'utf8').match(/(?<=shares\": \")(.*)(?=\", \"ch)/);
  var tags = fs.readFileSync('./json/'+file,'utf8').match(/(?<=tags\": \[)(.*)(?=\], \"sh)/);
  if ( author ) {
    x[author[0]] = (x[author[0]]||0) + 1;
    var s = (tags && JSON.parse('['+tags[0]+']').length) || 0;
    y[s] = (y[s]||0) + 1;
    n += s != 0;
    m = s > m ? s : m;
    // if (!y[lang[0]]) y[lang[0]] = [];
    // if (y[lang[0]].indexOf(author[0]) < 0) y[lang[0]].push(author[0]);
    // n++;
  }
});

// r.forEach((a,b)=>{
//   console.log(print(b),a[0],a[1]);
// })


// for (var t of Object.keys(x).sort(((a,b)=>x[a]-x[b]))) {
//   r[x[t]] = (r[x[t]]||0) + 1;
//   console.log(print(t),x[t]);
// } 

var print2 = s => (s + " ".repeat(5)).substr(0,5);

// for (var i=0; i<r.length; i++) {
//   console.log(print2(i),r[i]||0);
//   n += r[i]||0
// }

console.log(n);

for (var i=0; i<=m; i++)
    console.log(print2(i),y[i]||0);

// for (var i of Object.keys(y).sort((a,b)=>y[b].length-y[a].length))
//   if (y[i])
//     console.log(print2(i),y[i].length);

// var z = JSON.parse( "{u’el’: 6, u’en’: 2466, u’af’: 220, u’vi’: 124, u’ca’: 235, u’it’: 599, u’cy’: 193, u’cs’: 115, u’et’: 202, u’id’: 386, u’es’: 294, u’ru’: 62, u’nl’: 187, u’pt’: 422, u’no’: 300, u’zh-tw’: 2, u’tr’: 64, u’tl’: 142, u’lv’: 73, u’zh-cn’: 11, u’lt’: 111, u’th’: 27, u’ro’: 187, u’pl’: 339, u’fr’: 385, u’bg’: 14, u’hr’: 125, u’de’: 273, u’da’: 176, u’fa’: 0, u’None’: 66, u’fi’: 154, u’hu’: 87, u’ja’: 14, u’sq’: 193, u’ko’: 155, u’sv’: 123, u’mk’: 21, u’sk’: 155, u’so’: 93, u’uk’: 5, u’sl’: 158, u’sw’: 71}".replace(/u\’|\’/g,"\""));

// for (var i of Object.keys(z).sort((a,b)=>z[b]-z[a]))
//   if (z[i])
//     console.log(print2(i),z[i]);
