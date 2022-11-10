let sidebarVisible = false;
const sidebar = document.querySelector('#sidebar');
const sidebarArrow = document.querySelector('#arrow');

if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|BB|PlayBook|IEMobile|Windows Phone|Kindle|Silk|Opera Mini/i.test(navigator.userAgent)) {
    sidebarArrow.style.marginLeft = 78+"px";
    sidebarArrow.children[0].setAttribute('src', '/static/icons/left-arrow.png');
}

function openCloseSideBar() {
    const open = () => {
        sidebar.style.display = "block";
        sidebarArrow.style.marginLeft = 78+"px";
        sidebarArrow.children[0].setAttribute('src', '/static/icons/left-arrow.png');
    }
    const close = () => {
        sidebar.style.display = "none";
        sidebarArrow.style.marginLeft = 0+"px";
        sidebarArrow.children[0].setAttribute('src', '/static/icons/right-arrow.png');
    }
    if(!sidebarVisible){
        sidebarVisible = true;
        return open();
    }
    sidebarVisible = false;
    return close();
}