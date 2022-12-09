import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { searchUsers } from "../../store/users";
import { LoadingSpinner } from "../Elements";
import styles from "./NewMessage.module.css";
import { ProfilePicture } from "../Elements";
import { createNewRoom } from "../../store/rooms";
import { useHistory } from "react-router-dom";

const NewMessage = ({ onClose }) => {
  const dispatch = useDispatch();
  const history = useHistory();
  const searchResults = useSelector((state) =>
    Object.values(state.users.searchResults)
  );
  const [searchVal, setSearchVal] = useState(``);
  const [loaded, setLoaded] = useState(true);

  const updateSearchVal = (e) => {
    setLoaded(false);
    setSearchVal(e.target.value);
  };

  const handleClick = (userId) => async () => {
    try {
      const roomId = await dispatch(createNewRoom(userId));
      onClose();
      history.push(`/messages/${roomId}`);
    } catch (err) {}
  };

  useEffect(() => {
    let timeout;
    (async () => {
      try {
        await dispatch(searchUsers(searchVal));
      } catch (err) {}
      timeout = setTimeout(() => setLoaded(true), 500);
    })();

    return () => clearTimeout(timeout);
  }, [dispatch, searchVal]);

  return (
    <div className={styles.searchContainer}>
      <div className={styles.searchHeader}>
        <h2>New message</h2>
        <div className={styles.inputContainer}>
          <label>To:</label>
          <input
            type="text"
            placeholder="Search..."
            value={searchVal}
            onChange={updateSearchVal}
            className={styles.searchInput}
          />
        </div>
      </div>
      <div className={styles.searchResults}>
        {loaded ? (
          searchResults.map((result) => (
            <div
              className={styles.userContainer}
              onClick={handleClick(result.id)}
            >
              <div className={styles.profilePicture}>
                <ProfilePicture user={result} size={"large"} />
              </div>
              <div className={styles.userDetails}>
                <p className={styles.username}>{result.username}</p>
                <p className={styles.fullName}>{result.full_name}</p>
              </div>
            </div>
          ))
        ) : (
          <div className={styles.loadingSpinner}>
            <LoadingSpinner />
          </div>
        )}
      </div>
    </div>
  );
};

export default NewMessage;
