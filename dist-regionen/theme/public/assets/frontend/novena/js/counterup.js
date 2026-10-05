/*
https://www.cssscript.com/demo/number-countup-animation-counter/
 */
const counters = document.querySelectorAll('.counterup');
for(let n of counters) {
    const updateCount = () => {
        const target = + n.getAttribute('data-target');
        const count = + n.innerText;
        const speed = 5000;

        const inc = target / speed;

        if(count < target) {
            n.innerText = Math.ceil(count + inc);
            setTimeout(updateCount, 1);
        } else {
            n.innerText = target;
        }
    }
    updateCount();
}
