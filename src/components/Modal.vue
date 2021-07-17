<template>
    <div class="backdrop" @click.self='closeModal'>
        <div class="modal" :class="{highlight: theme === 'highlight'}">
            <slot></slot>
            <div class="actions">
                <slot name="links"></slot>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: ['header', 'text', 'theme'],
        methods: {
            closeModal() {
                this.$emit('closeModal')
            }
        }
    }
</script>

<style>
    .modal {
        width: 400px;
        padding: 20px;
        margin: 100px auto;
        background: white;
        border-radius: 10px;
    }

    .backdrop {
        top: 0;
        position: fixed;
        background: rgba(0, 0, 0, 0.5);
        width: 100%;
        height: 100%;
    }

    .modal h1 {
        color: #96494f;
        border: none;
        padding: 0;

    }

    .modal.highlight {
        color: #ffffff;
        background: #96494f;
    }

    .modal.highlight h1 {
        color: #ffffff;
    }
</style>