import React from 'react'
import { Link } from 'react-router-dom'

const Header = () => {
    return (
        <div className="Header">
            <div className="Navbar">
                <nav className="navbar navbar-light bg-light">

                    <Link className="navbar-brand" to="/">
                        Mars
                    </Link>

                </nav>

            </div>
        </div>
    );
}

export default Header;