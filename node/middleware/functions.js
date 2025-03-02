export function getDateTime() {
    let dateObj = new Date();

    const time = dateObj.toTimeString().slice(0, 5);
    const day =
        dateObj.getDate() > 9 ? dateObj.getDate() : `0${dateObj.getDate()}`;
    const month = dateObj.getMonth() + 1;
    const year = dateObj.getFullYear();

    const dateTime = {
        date: `${day}/${month}/${year}`,
        time: time,
    };

    return dateTime;
}
