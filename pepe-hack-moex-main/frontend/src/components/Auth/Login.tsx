import React from "react";
import {useFormik} from "formik";
import {Button, Flex, Input, Typography} from "antd";

const {Text, Title} = Typography;

interface LoginPropsType {
    setRegisterForm: () => void;
}

const Login: React.FC<LoginPropsType> = (props) => {
    const formik = useFormik({
        initialValues: {
            email: "",
            password: "",
        },
        onSubmit: (values) => {
            // todo: api response
            // authAPI.postAuthLogin(values, (response: Response) => {
            //     if (response.status === 200) {
            //         props.setAuth();
            //     }
            // });
        },
    });

    return (
        <form onSubmit={formik.handleSubmit}>
            <Flex vertical align="center" justify={"center"} gap={6}>
                <Title level={3}>
                    Вход
                </Title>
                <Input placeholder="Email" />
                <Input placeholder="password" />
                <Flex align="center" justify={"center"} gap={16}>
                    <Button
                        size="large"
                    >
                        Войти
                    </Button>
                </Flex>

                <Button
                    size="large"
                    onClick={props.setRegisterForm}
                >
                    Зарегистрироваться
                </Button>
            </Flex>
        </form>
    );
};

export default Login;
