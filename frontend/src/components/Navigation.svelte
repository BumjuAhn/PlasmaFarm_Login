<script>
    import { link } from 'svelte-spa-router'
    import { page, keyword, access_token, username, is_login } from "../lib/store"
</script>

<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/" 
            on:click="{() => {$keyword = '', $page = 0}}">PlasmaFarm</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" />
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                {#if $is_login }
                    <li class="nav-item">
                        <a use:link href="/user-login" class="nav-link" on:click={() => {
                            $access_token = ''
                            $username = ''
                            $is_login = false
                        }}>로그아웃 ({$username})</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/control">Control</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/board">Board</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/about">About</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/contact">Contact</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-create">회원가입</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-login">로그인</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/control">Control</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/board">Board</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/about">About</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/contact">Contact</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>