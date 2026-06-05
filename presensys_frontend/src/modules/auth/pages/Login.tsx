import "./login.css";

export default function Login() {
  return (
    <div className="login-container">

        <div className="login-card">

            <h1>Bem-vindo ao sistema de checklists</h1>
            <h2>Faça login e acompanhe os checklists da Macro Ambiental</h2>

            <form>

                <div className="input-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" placeholder="Digite seu username" id="username" name="username" required />   
                </div>

                <div className="input-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" placeholder="Digite sua senha" id="password" name="password" required />
                </div>
                <button type="submit">Login</button>


            </form>

     
            </div>
        </div>
    );
}       