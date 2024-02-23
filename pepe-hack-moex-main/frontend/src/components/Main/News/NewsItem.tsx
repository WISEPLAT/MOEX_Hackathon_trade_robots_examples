import React, {FC} from 'react';
import {Card, Divider, Flex, Image, Typography} from 'antd';
import {useNavigate} from "react-router-dom";
import styles from "./News.module.scss";

const NewsItem: FC<{ title: string, description: string, imgSrc: string }> = ({title, description, imgSrc}) => {
    const navigate = useNavigate();

    function onClick(): void {
    }

    return (
        <Flex flex="1 1 242px" style={{height: '100%', width: '100%'}}>
            <Card bordered={true} size={"small"}
                  hoverable={true}
                  className={styles.newsItem}
                  style={{boxShadow: '0px 4px 4px 0px rgba(0, 0, 0, 0.25)', paddingBottom: 0}}
                  bodyStyle={{padding: 0}}
                  onClick={onClick}
                  cover={<img
                      height={124}
                      src={imgSrc || 'https://img.freepik.com/premium-vector/growth-arrow-financial-graph-on-digital-technology-strategy-background_701664-107.jpg'}
                  />}
            >
                <Flex vertical style={{paddingBottom: 30, paddingLeft: 12, paddingRight: 12, paddingTop: 10}}>
                    <Typography.Text style={{
                        fontSize: 11,
                        paddingBottom: 9,

                    }}>12 Декабря</Typography.Text>
                    <Typography.Text strong className={styles.title} style={{
                        fontSize: 13, marginBottom: 16, textOverflow: 'ellipsis'
                    }}>{title}</Typography.Text>
                    <Typography.Text style={{
                        fontSize: 11,
                        maxHeight: '100%',
                        minHeight: 0,
                        flexBasis: 66,
                        textOverflow: 'ellipsis',
                        overflow: 'hidden'
                    }}>{description}</Typography.Text>
                </Flex>
            </Card>
        </Flex>
    );
};

export default NewsItem;
