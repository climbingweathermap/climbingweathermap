<template>
    <div class="content  vh-100">
        <NavBar class="p-2 item-top" />
        <Options class="p-2 item-top" />
        <Map class=" p-2 item" />
        <Footer class="p-2 item-bottom" />
    </div>
</template>

<script>
    import Modal from './components/Modal.vue'
    import NavBar from './components/NavBar.vue'
    import Footer from './components/Footer.vue'
    import Options from './components/Options.vue'
    import Map from './components/Map.vue'
    export default {
        name: 'App',
        components: {
            Modal,
            NavBar,
            Footer,
            Map,
            Options
        },
        data: function() {
            return {}
        },
        methods: {}
    };
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        ;
    }

    .content {
        display: flex;
        align-items: stretch;
        align-content: stretch;
        flex-direction: column;
        justify-content: space-evenly;
        flex-wrap:
    }

    .item {
        flex-grow: 4;
        order: 2;
    }

    .item-top {
        flex-grow: 0;
        order: 1;
    }

    .item-bottom {
        flex-shrink: 0;
        order: 3;
    }
</style>