const dayOfWeekDigit = new Date([], {"timeZone": "Asia/Tehran"}).getDay();
console.log(dayOfWeekDigit);

const dayOfWeekName = new Date().toLocaleString(
'default', {weekday: 'long'}
);

switch(dayOfWeekName) {
    case "Saturday":
        document.write("شنبه");
        break;
    case "Sunday":
        document.write("یک شنبه");
        break;
    case "Monday":
        document.write("دو شنبه");
        break;
    case "Tuesday":
        document.write("سه شنبه");
        break;
    case "Wednesday":
        document.write("چهار شنبه");
        break;
    case "Thursday":
        document.write("پنج شنبه");
        break;
    case "Friday":
        document.write("جمعه");
        break;
}
