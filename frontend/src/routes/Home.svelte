<script>
    import { link } from 'svelte-spa-router';
    import plasmafarmhero from '../assets/plasma-farm-hero.jpg';
    import ecofriendly from '../assets/icons/eco-friendly.webp';
    import fastgrowth from '../assets/icons/fast-growth.webp';
    import diseasecontrol from '../assets/icons/disease-control.webp';

    const features = [
        {
            title: '환경 친화적',
            description: '화학물질 사용 없이 지속 가능한 농업 환경을 조성합니다.',
            icon: ecofriendly,
            alt: 'Eco-friendly',
        },
        {
            title: '작물 성장 가속화',
            description: '작물의 성장 속도와 품질을 동시에 향상시킵니다.',
            icon: fastgrowth,
            alt: 'Fast Growth',
        },
        {
            title: '병충해 방제',
            description: '플라즈마 기술로 자연스럽고 효과적으로 병충해를 억제합니다.',
            icon: diseasecontrol,
            alt: 'Disease Control',
        },
    ];
</script>

<div class="container my-5">
    <!-- Plasma Farm Header -->
    <header class="text-center my-5">
        <h1 class="display-1 text-success fw-bold">BOmBzOO's Plasma Farm</h1>
        <p class="lead fs-4 text-muted mt-3">
            혁신적인 플라즈마 기술로 농업의 한계를 뛰어넘습니다.
        </p>
    </header>

    <!-- Hero Section -->
    <section class="row align-items-center">
        <div class="col-md-6">
            <h2 class="text-success fw-bold mb-4">플라즈마와 농업의 만남</h2>
            <p class="text-muted fs-5">
                플라즈마 기술은 작물 성장과 생산성 향상, 병충해 방제, 그리고 환경친화적 솔루션을 제공합니다. 
                BOmBzOO의 Plasma Farm은 지속 가능한 농업을 구현하며, 여러분의 농업 혁신에 기여합니다.
            </p>
            <a use:link href="/about" class="btn btn-success btn-lg mt-3">더 알아보기</a>
        </div>
        <div class="col-md-6">
            <img 
                src={plasmafarmhero} 
                alt="Plasma Farm Hero Image" 
                class="img-fluid rounded" 
                aria-hidden="true"
            />
        </div>
    </section>

    <!-- Features Section -->
    <section class="mt-5">
        <h2 class="text-center text-success fw-bold mb-5">플라즈마 농업의 주요 혜택</h2>
        <div class="row text-center">
            {#each features as feature}
                <div class="col-md-4">
                    <img src={feature.icon} alt={feature.alt} class="mb-4" width="300" />
                    <h4 class="fw-bold">{feature.title}</h4>
                    <p class="text-muted">{feature.description}</p>
                </div>
            {/each}
        </div>
    </section>

    <!-- Call to Action -->
    <section class="text-center mt-5">
        <h2 class="text-success fw-bold">플라즈마 농업의 미래에 동참하세요</h2>
        <p class="text-muted fs-5 mt-3">
            BOmBzOO와 함께 지속 가능한 농업의 새로운 지평을 열어가세요.
        </p>
        <a use:link href="/contact" class="btn btn-outline-success btn-lg">문의하기</a>
    </section>

    <!-- Footer -->
    <footer class="text-center mt-5">
        <p class="text-muted small">© 2024 BOmBzOO's Plasma Farm. 모든 권리 보유.</p>
    </footer>
</div>
