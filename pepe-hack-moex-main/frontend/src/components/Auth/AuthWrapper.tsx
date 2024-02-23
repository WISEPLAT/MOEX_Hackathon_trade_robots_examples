import React, {useEffect, useState} from "react";
import styles from "./Auth.module.scss";
import Login from "./Login";
import {Card, Col, Row} from "antd";
import Register from "./Register";

enum TypeAuth {
    auth, register
}

const AuthWrapper: React.FC<any> = (props) => {
    const [type, setType] = useState<TypeAuth>(TypeAuth.auth);

    useEffect(() => {
        // if (props.auth) {
        //   navigate(prevLocation, { replace: true });
        // }
    }, [props.auth]);

    return (
        <Row className={styles.container} justify={'center'} align={'middle'} >
            <Col flex="1 1 450px">
                <Card>
                    {type === TypeAuth.auth ? <Login setRegisterForm={() => setType(TypeAuth.register)}/> :
                        <Register setAuthForm={() => setType(TypeAuth.auth)}/>}
                </Card>
            </Col>
            <ul className={styles.particles}>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
            </ul>
        </Row>
    );
};

export default AuthWrapper;
