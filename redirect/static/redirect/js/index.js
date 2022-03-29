
function toggleUrlDisplay(ownObject) {
    const targetId = 'el' + ownObject.getAttribute('data-value');
    const target = document.getElementById(targetId);
    if (ownObject.innerHTML == 'Show') {
        target.style.whiteSpace = 'normal';
        target.style.wordBreak = 'break-word';
        ownObject.innerHTML = 'Hide';
    } else {
        target.style.whiteSpace = 'nowrap';
        target.style.wordBreak = 'normal';
        ownObject.innerHTML = 'Show';
    }
}

function toggleDeletePanel(idBase, direction) {
    const normalPanelId = 'np' + idBase;
    const normalPanel = document.getElementById(normalPanelId);
    const deletePanelId = 'dp' + idBase;
    const deletePanel = document.getElementById(deletePanelId);
    if (direction == 'open') {
        normalPanel.style.display = 'none';
        deletePanel.style.display = 'flex';
    } else {
        normalPanel.style.display = 'flex';
        deletePanel.style.display = 'none';
    }
}

function deleteCouplet(targetInUrl) {
    ajaxPost(targetInUrl, 'delete');
}

function displayCouplet(couplet) {
    const target = document.querySelector('#couplet-display');
    const coupletDiv = document.createElement('div');
    coupletDiv.innerHTML = `
                            <div id="${couplet[0]}" class="url-display-box">
                                <div class="url-display-box-left">
                                    <div style="word-break: break-word;">urlgogo.com/${couplet[0]} redirects to...</div>
                                    <div class="ellipsis-line" id="el${couplet[0]}">
                                        <a href="${couplet[1]}">${couplet[1]}</a>
                                    </div>
                                </div>
                                <div id="np${couplet[0]}" class="url-display-box-right">
                                    <button onclick="toggleDeletePanel('${couplet[0]}', 'open');">Delete</button>
                                    <button onclick="toggleUrlDisplay(this);" data-value="${couplet[0]}">Show</button>
                                </div>
                                <div id="dp${couplet[0]}" style="display: none;" class="url-display-box-right">
                                    Delete?
                                    <br>
                                    <button onclick="deleteCouplet('${couplet[0]}');">Yes</button>
                                    <button onclick="toggleDeletePanel('${couplet[0]}', 'close');">No</button>
                                </div>
                            </div>
                            `
    target.appendChild(coupletDiv);
}

function addLocally(coupletList) {
    let storedCoupletList = JSON.parse(sessionStorage.getItem('storedCoupletList'));
    storedCoupletList = storedCoupletList.concat(coupletList);
    sessionStorage.setItem('storedCoupletList', JSON.stringify(storedCoupletList));
}

function removeLocally(inUrl) {
    let storedCoupletList = JSON.parse(sessionStorage.getItem('storedCoupletList'));
    let targetIndex = -1;
    for (let i = 0; i < storedCoupletList.length; i++) {
        if (storedCoupletList[i][0] == inUrl) {
            targetIndex = i;
            break;
        }
    }
    storedCoupletList.splice(targetIndex, 1);
    sessionStorage.setItem('storedCoupletList', JSON.stringify(storedCoupletList));
}

function getLocalList(userId) {
    let storedCoupletList = JSON.parse(sessionStorage.getItem('storedCoupletList'));
    if (storedCoupletList == null) {
        storedCoupletList = [];
        if (userId == -1) {
            sessionStorage.setItem('storedCoupletList', JSON.stringify(storedCoupletList));
        }
    }
    return storedCoupletList;
}  

function ajaxPost(dataPost, type, merge=false) {
    
    dataPost = [dataPost, merge];
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    jQuery.ajaxSetup({
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            }
    });
    
    if (type == 'add') {
        postUrl = '/e35e6da7bdbc4c0bec05f32bea5c6ae1/';
    } else {
        postUrl = '/ec8db41d74c36b954821ab64f8226de0/';
    }
    
    jQuery.ajax({
        type: 'POST',
        url: postUrl,
        data: {
            dataPost: JSON.stringify(dataPost)
        },
        success: function() {
            if (type == 'add') {
                document.querySelector('#in-url-input').value = '';
                document.querySelector('#out-url-input').value = '';
                const coupletList = dataPost[1];
                for (let i = 0; i < coupletList.length; i++) {
                    displayCouplet(coupletList[i]);
                }
                if (dataPost[0] == -1) {
                    addLocally(coupletList);
                }
                if (merge) {
                    sessionStorage.clear();
                    setTimeout(function() {
                        document.querySelector('#dismiss-merge').click();
                    });
                }
            } else {
                const target = document.getElementById(dataPost);
                target.outerHTML = '';
                if (sessionStorage.length > 0) {
                    removeLocally(dataPost);
                }
            }
        },
        error: function() {
            if (type == 'add') {
                alert('That URL (in the top box) is taken.');
            } else {
                alert('Something went wrong.');
            }
        }
    });
}

function setIndex() {

    const userId = JSON.parse(document.getElementById('user_id').textContent);
    let coupletList = JSON.parse(document.getElementById('couplet_list').textContent);
    let storedCoupletList = getLocalList(userId);

    if (userId != -1) {
        if (storedCoupletList.length != 0) {
            setTimeout(function() {
                document.querySelector('#merge-modal-trigger').click();
            });
        }
    } else {
        coupletList = storedCoupletList;
    }
    
    for (let i = 0; i < coupletList.length; i++) {
        displayCouplet(coupletList[i]);
    }
    
    document.querySelector('#set-url-button').onclick = function() {
        const inUrl = document.querySelector('#in-url-input').value;
        const outUrl = document.querySelector('#out-url-input').value;
        if (outUrl.slice(0, 7) == 'http://' || outUrl.slice(0, 8) == 'https://') {
            const dataPost = [userId, [[inUrl, outUrl]]];
            ajaxPost(dataPost, 'add');
        } else {
            alert('The URL to go to is not valid. It must start with http:// or https://.');
        }
    }
    
    document.querySelector('#merge-button').onclick = function() {
        const dataPost = [userId, getLocalList()]
        ajaxPost(dataPost, 'add', merge=true);
    }
    
    document.querySelector('#in-url-input').addEventListener('keyup', function(event) {
        if (event.keyCode === 13) {
            document.querySelector('#set-url-button').click();
        }
    });
    
    document.querySelector('#out-url-input').addEventListener('keyup', function(event) {
        if (event.keyCode === 13) {
            document.querySelector('#set-url-button').click();
        }
    });
}






