<template>
    <teleport to=".my-navbar">
        <NavBar />
    </teleport>
    <teleport to=".footer">
        <Footer />
    </teleport>
    <Map />
</template>

<script>
    import Modal from './components/Modal.vue'
    import NavBar from './components/NavBar.vue'
    import Footer from './components/Footer.vue'
    import Map from './components/Map.vue'
    export default {
        name: 'App',
        components: {
            Modal,
            NavBar,
            Footer,
            Map,
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
</style>