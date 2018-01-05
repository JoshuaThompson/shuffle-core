$(document).ready(function() {
    $('.language-select').select2();

    $.post( "/get-matching-streams", function(data) {
        $('.stream').html(`<iframe
            src="http://player.twitch.tv/?channel=${data.name}&muted=true"
            height="100%"
            width="100%"
            frameborder="0"
            scrolling="no"
            allowfullscreen="true">
        </iframe>`)

        $('.chat').html(`<iframe frameborder="0"
            scrolling="yes"
            id="${data.name}"
            src="http://www.twitch.tv/${data.name}/chat?darkpopout"
            height="100%"
            width="100%">
        </iframe>`)

        $('.stream-title').html(`<h1 class="title">${data.name}</h1>`)
        $('.stream-status').html(`
            <div>
                <img class="logo" src="${data.logo}" />
            </div>
            <div>
                <p class="subtitle is-6 status-text">${data.status}</p>
                <p class="subtitle is-6 status-text">Streaming ${data.game}</p>
                <div class="stats">
                    <div class="tw-stat" data-a-target="channel-viewers-count">
                        <span class="tw-stat__icon"><figure style="fill: #ec1313 !important;" class="tw-svg"><svg class="tw-svg__asset tw-svg__asset--glyphlive tw-svg__asset--inherit" width="16px" height="16px" version="1.1" viewBox="0 0 16 16" x="0px" y="0px"><path clip-rule="evenodd" d="M11,14H5H2v-1l3-3h2L5,8V2h6v6l-2,2h2l3,3v1H11z" fill-rule="evenodd"></path></svg></figure></span>
                        <span style="color: #ec1313 !important;" class="tw-stat__value" data-a-target="tw-stat-value">${data.viewers}</span>
                    </div>
                    <div class="tw-stat" data-a-target="total-views-count">
                        <span class="tw-stat__icon"><figure class="tw-svg"><svg class="tw-svg__asset tw-svg__asset--glyphviews tw-svg__asset--inherit" width="16px" height="16px" version="1.1" viewBox="0 0 16 16" x="0px" y="0px"><path clip-rule="evenodd" d="M11,13H5L1,9V8V7l4-4h6l4,4v1v1L11,13z M8,5C6.344,5,5,6.343,5,8c0,1.656,1.344,3,3,3c1.657,0,3-1.344,3-3C11,6.343,9.657,5,8,5z M8,9C7.447,9,7,8.552,7,8s0.447-1,1-1s1,0.448,1,1S8.553,9,8,9z" fill-rule="evenodd"></path></svg></figure></span>
                        <span class="tw-stat__value" data-a-target="tw-stat-value">${data.views}</span>
                    </div>
                </div>
            </div>
        `)
    });
});