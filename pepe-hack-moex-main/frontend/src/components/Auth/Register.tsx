import React from "react";
import {useFormik} from "formik";
import {Button, Flex, Input, Typography} from "antd";

const {Text, Title} = Typography;

interface RegisterPropsType {
    // setLoginForm: () => void;
    // setIsAuth: () => void;
    setAuthForm: () => void;
}

const Register: React.FC<RegisterPropsType> = (props) => {
    const formik = useFormik({
        initialValues: {
            email: "",
            name: "",
            surname: "",
            patronymic: "",
            password: "",
        },
        onSubmit: (values) => {
            // authAPI.postAuthRegister(values).then(() => {
            //   authAPI.postAuthLogin(
            //     {
            //       email: values.email,
            //       password: values.password,
            //     },
            //     (response: Response) => {
            //       if (response.status === 200) {
            //         props.setIsAuth();
            //       }
            //     },
            //   );
            // });
        },
    });

    return (
        <form onSubmit={formik.handleSubmit}>
            <Flex vertical align="center" justify={"center"} gap={6}>
                <Title level={3}>
                    Регистрация
                </Title>
                <Input placeholder="Имя"/>
                <Input placeholder="password"/>
                <Button
                    size="large"
                >
                    Зарегистрироваться
                </Button>
                <Button
                    size="large"
                    onClick={props.setAuthForm}
                >
                    У меня уже есть аккаунт
                </Button>
            </Flex>
        </form>
    );
};

export default Register;
