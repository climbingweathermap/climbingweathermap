<template>
    <div class="backdrop" @click.self='closeModal'>
        <div class="mymodal">
            <h1>{{title}}</h1>
            <br>
            <p>{{text}}</p>
        </div>
    </div>
</template>

<script>
    export default {
        props: ['title', 'text'],
        methods: {
            closeModal() {
                this.$emit('close')
            }
        }
    }
</script>

<style>
    .mymodal {
        width: 80vw;
        height: 10vh;
        padding: 20px;
        margin: 100px auto;
        background: #F6F7F8;
        border-radius: 10px;
        z-index: 4;
        text-align: center;
    }

    .backdrop {
        top: 0;
        position: fixed;
        background: rgba(0, 0, 0, 0.5);
        width: 100%;
        height: 100%;
        z-index: 1;

    }

    .modal h1 {
        color: #011627;
        border: none;
        padding: 0;

    }
</style>