<template>
    <div class="iconBox">
        <div>
            <img :src="summaryIcon" height="32" />
        </div>
        <div>
            <img :src="rainIcon" height="32" />
        </div>
        <div>
            <p>{{temp.toFixed(1)}}</p>
        </div>
        <div v-if="largeIcon">
            <p>{{title}}</p>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default {
        name: "Icon",
        props: {
            title: String,
            summaryIcon: String,
            rainIcon: String,
            temp: Number,
            zoom: Number
        },
        methods: {
            toFixed: (value, precision) => {
                var power = Math.pow(10, precision || 0);
                return String(Math.round(value * power) / power);
            }
        },
        computed: {
            largeIcon() {
                return (this.zoom > 10)
            }
        },
    }
</script>

<style>
    .iconBox {
        display: flex;
        background: var(--bs-dark2);
        color: var(--bs-light);
        padding: 5px;
        max-height: 32px;
        overflow: hidden;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        border-radius: 5px;

    }

    .iconBox p {
        margin: 0;
        margin-left: 5px;
        max-width: 80px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap
    }
</style>