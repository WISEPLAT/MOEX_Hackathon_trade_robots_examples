import React, {FC} from 'react';
import {Button, Carousel as AntCarousel, Flex, Image, Typography} from 'antd';
import './Carousels.scss';
import img2 from './2.jpg';
import img3 from './3.jpg';
import {useNavigate} from "react-router-dom";

const contentStyle: React.CSSProperties = {
    margin: '0 auto',
    height: '300px',
    color: '#fff',
    textAlign: 'center',

    padding: '10px 50px',
    maxWidth: '1300px',
};

const Carousel: FC = () => {
    const navigate = useNavigate();

    function onClick(): void {
        navigate(`/bot`);
    }

    return (
        <div className={'-'}>
            <AntCarousel className={'gradient-background'} style={{borderRadius: 10, overflow: 'hidden'}}>
                <div>
                    <Flex align={'center'} justify={'space-between'} style={contentStyle}>
                        <Typography.Paragraph
                            style={{color: 'white', fontSize: '1.5em', textAlign: "left", marginBottom: 0}}>
                            Надежные инвестиции с ботом от <Typography.Text type={'danger'} strong
                                                                            style={{fontSize: '1em'}}>AI
                            Биржа</Typography.Text>
                        </Typography.Paragraph>
                        <div style={{
                            width: '75.264px',
                            height: '360.432px',
                            transform: 'rotate(11.913deg)',
                            flexShrink: 0,
                            background: 'white',
                            zIndex: 1
                        }}/>
                        <Button style={{fontSize: 20, width: 250, height: 58, fontWeight: 'bold'}} onClick={onClick}>
                            Перейти на бота
                        </Button>
                    </Flex>
                </div>
                <div>
                    <Flex align={'center'} justify={'space-between'}
                          style={{...contentStyle, maxWidth: 'max-content', padding: 0, paddingLeft: 50}}>
                        <Typography.Paragraph style={{color: 'white', fontSize: '1.5em', textAlign: "left"}}>
                            Оптимизируй свои инвестиции с нашим торговым ботом, созданным искусственным интеллектом!
                            Доверь торговлю на бирже надежному алгоритму, который работает для тебя 24/7
                        </Typography.Paragraph>
                        <div style={{
                            width: '200.083px',
                            height: '370.161px',
                            transform: 'rotate(11.913deg) translateX(50%)',
                            background: 'red',
                            zIndex: 1
                        }}/>
                        <Image src={img2} preview={false}/>
                    </Flex>
                </div>
                <div>
                    <Flex align={'center'} justify={'space-between'}
                          style={{...contentStyle, maxWidth: 'max-content', padding: 0, paddingLeft: 50}}>
                        <Typography.Paragraph style={{color: 'white', fontSize: '1.5em', textAlign: "left"}}>
                            Получай точные прогнозы акций в режиме реального времени от искусственного интеллекта. Наш
                            сайт предоставляет уникальные аналитические данные для успешного трейдинга на финансовых
                            рынках.
                        </Typography.Paragraph>
                        <div style={{
                            width: '200.083px',
                            height: '370.161px',
                            transform: 'rotate(11.913deg) translateX(50%)',
                            background: 'red',
                            zIndex: 1
                        }}/>
                        <Image src={img3} preview={false}/>
                    </Flex>
                </div>
            </AntCarousel>
        </div>
    );
};

export default Carousel;
