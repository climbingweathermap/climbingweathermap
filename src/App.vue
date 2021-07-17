<template>
    <teleport to=".my-navbar">
        <NavBar />
    </teleport>
    <teleport to=".footer">
        <Footer />
    </teleport>
    <div v-if="showLocWarning">
        <Modal :title="LocWarning" :text="LocWarningBody" @close="toggleLocWarning" />
    </div>
    <Map @locationNotFound="toggleLocWarning" />
</template>

<script>
    import Modal from './components/Modal.vue'
    import NavBar from './components/NavBar.vue'
    import Map from './components/Map.vue'
    import Footer from './components/Footer.vue'
    export default {
        name: 'App',
        components: {
            Modal,
            NavBar,
            Map,
            Footer
        },
        data() {
            return {
                showLocWarning: false,
                LocWarning: "Your location could not be found",
                LocWarningBody: "Ensure location detection is permitted"
            }
        },
        methods: {
            toggleLocWarning() {
                this.showLocWarning = !this.showLocWarning;
            }
        }
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