<script>
  import Navigation from "./components/Navigation.svelte"
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Control from "./routes/Control.svelte"
  import Board from "./routes/Board.svelte"
  import Detail from "./routes/Detail.svelte"
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import QuestionModify from "./routes/QuestionModify.svelte"
  import AnswerModify from "./routes/AnswerModify.svelte"
  import About from "./routes/About.svelte"
  import Contact from "./routes/Contact.svelte"
  import Footnote from "./components/Footnote.svelte"

  const routes = {
    '/': Home,
    '/control': Control,
    '/board': Board,
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
    '/about': About,
    '/contact': Contact,
  }
</script>

<Navigation />
<Router {routes}/>
<Footnote />
