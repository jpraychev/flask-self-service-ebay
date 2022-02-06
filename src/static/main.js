/** 
* @summary Update HTML element with id of note, after file is being deleted from the system
*/
const udpateNote = () => {
    $('#note').html('Note: file has been deleted')
}

/**
* @summary Download counter indicating to user how much time they have got to download
their file. Once the timer expires, we update the note to the user, clean up (stop) the setted interval
and redirect the user directyly to home page to avoid generating new files.
* @param {int} step - Decrease step of the countdown timer
*/
const downloadCountdown = (step) => {
    timer = $('#download_timer')
    currTime = parseInt(timer.html())
    timer.html(currTime - step)
    if (currTime <= 1) {
        udpateNote()
        clearInterval(timerInterval)
        window.location.href = '/'
    } 
}
const timerInterval = setInterval(downloadCountdown, 1000, 1)