var fs = require('fs');

var print = s => (s + " ".repeat(20)).substr(0,20);

var r = [], x = {}, y={}, z=[], n=0;

  // var body = JSON.parse(fs.readFileSync('./json/'+file,'utf8').replace(/, \"disc.+/,'}')); 
var channels = fs.readFileSync('./all_charts.txt','utf8').match(/(?<=channels\/)([0-9]+)(?=\/)/g);
channels.forEach(a=>x[a]=(x[a]||0)+1);
for (i in x) {
  r[x[i]] = (r[x[i]]||0) + 1;
  y[i/1e5|0]=(y[i/1e5|0]||0)+1;
  n++
  if (x[i]>10) z[x[i]] = (z[x[i]]||[]).concat(i);
}
console.log(y);
console.log(n);
console.log(z);
// if ( channels ) {
//   console.log(n)
// }

// r.forEach((a,b)=>{
//   console.log(print(b),a[0],a[1]);
// })


// for (var t of Object.keys(x).sort(((a,b)=>x[a]-x[b]))) {
//   r[x[t]] = (r[x[t]]||0) + 1;
//   console.log(print(t),x[t]);
// } 

var print2 = s => (s + " ".repeat(5)).substr(0,5);

for (var i=0; i<r.length; i++) {
  console.log(print2(i),r[i]||0);
}

// console.log(n);