import { useSelector, useDispatch } from "react-redux";
import { NavLink, Link, useHistory } from "react-router-dom";
import { useState } from "react";
import NavItem from "./NavItem";
import styles from "./NavBar.module.css";
import MoreItem from "./MoreItem";
import { logout } from "../../store/session";
import Search from "../Search/Search";

const NavBar = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  const [showMore, setShowMore] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const user = useSelector((state) => state.session.user);
  const links = [
    // { icon: "Logo", path: "/" },
    { icon: "Instagram", path: "/" },
    { icon: "Home", path: "/" },
    { icon: "Search", path: "/search" },
    { icon: "Explore", path: "/users" },
    { icon: "Messages", path: "/messages" },
    { icon: "Notifications", path: "/notifications" },
    { icon: "Create", path: "/create" },
    { icon: "Profile", path: `/users/${user.id}` },
    { icon: "More", path: "#" },
  ];

  const loggedInNav = (
    <>
      <li>
        <NavLink to="/login" exact={true} activeClassName={styles.active}>
          Login
        </NavLink>
      </li>
      <li>
        <NavLink to="/sign-up" exact={true} activeClassName={styles.active}>
          Sign Up
        </NavLink>
      </li>
    </>
  );

  const handleShowMore = (e) => setShowMore((prev) => !prev);
  const handleLogout = async (e) => {
    await dispatch(logout());
    history.push("/");
  };

  return (
    <>
      <ul className={`${styles.navBar} ${showSearch && styles.miniNavBar}`}>
        <div>
          {user &&
            links.slice(0, links.length - 1).map(({ icon, path }, idx) =>
              icon === "Search" ? (
                <div
                  key={idx}
                  // className={showSearch && styles.activeSearch}
                  onClick={() => setShowSearch((state) => !state)}
                >
                  <NavItem type={icon} showSearch={showSearch} />
                </div>
              ) : (
                <NavLink
                  key={idx}
                  to={path}
                  exact={true}
                  className={styles.navLink}
                  activeClassName={styles.active}
                >
                  <NavItem type={icon} showSearch={showSearch} />
                </NavLink>
              )
            )}
        </div>
        {user && (
          <div className={styles.moreLink} onClick={handleShowMore}>
            <div
              className={showMore ? styles.moreDropDown : styles.hideDropDown}
              id="menu-dropdown"
            >
              <NavLink
                to="/account/edit"
                exact={true}
                className={styles.navLink}
              >
                <MoreItem type="Settings" />
              </NavLink>
              <NavLink to="/saved" exact={true} className={styles.navLink}>
                <MoreItem type="Saved" />
              </NavLink>
              <NavLink to="/report" exact={true} className={styles.navLink}>
                <MoreItem type="Report a problem" />
              </NavLink>
              <NavLink to="#" exact={true} className={styles.navLink}>
                <MoreItem type="Switch accounts" />
              </NavLink>
              <NavLink to="#" exact={true} className={styles.navLink}>
                <MoreItem type="Log Out" onClick={handleLogout} />
              </NavLink>
              {/* <LogoutButton style={styles.navLink} /> */}
            </div>
            <NavItem type="More" />
          </div>
        )}
        {!user && loggedInNav}
      </ul>
      {/* {showSearch && <Search onClose={() => setShowSearch(false)} />} */}
    </>
  );
};

export default NavBar;
