export function formatDate(date) {
    return weekdays[date.getDay()] + ", " +
        date.getDate() + nth(date.getDate()) + " " +
        months[date.getMonth()] + " " +
        date.getFullYear();
}

export function yymmddToUnix(yymmdd) {
  return new Date(Math.floor(2000 + yymmdd / 10000), Math.floor((yymmdd % 10000) / 100) - 1, Math.floor(yymmdd % 100)).getTime() / 1000;
}

export function unixToYymmdd(unix) {
  const date = new Date(unix * 1000);
  return (date.getFullYear() - 2000)
    + ('0' + (date.getMonth() + 1)).slice(-2)
    + ('0' + date.getDate()).slice(-2);
}

const weekdays = [
    "Sunday", "Monday", "Tuesday",
    "Wednesday", "Thursday", "Friday",
    "Saturday"
  ], months = [
    "January", "February", "March",
    "April", "May", "June", "July",
    "August", "September", "October",
    "November", "December"
  ];

function nth(d) {
    if(d>3 && d<21) return 'th';
    switch (d % 10) {
          case 1:  return "st";
          case 2:  return "nd";
          case 3:  return "rd";
          default: return "th";
    }
  }