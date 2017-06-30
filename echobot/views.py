# line_echobot/echobot/views.py

# WebhookParser version


from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    if event.message.text=='text' :
                        reply=TextSendMessage(text="just text")
                    elif event.message.text=='image' :
                        reply=ImageSendMessage(
                            original_content_url='https://example.com/original.jpg',
                            preview_image_url='https://example.com/preview.jpg'
                        )
                    elif event.message.text=='video' :
                        reply=VideoSendMessage(
                            original_content_url='https://example.com/original.mp4',
                            preview_image_url='https://example.com/preview.jpg'
                        )
                    elif event.message.text=='audio' :
                        reply=AudioSendMessage(
                            original_content_url='https://example.com/original.m4a',
                            duration=240000
                        )
                    elif event.message.text=='location' :
                        reply= LocationSendMessage(
                            title='my location',
                            address='Tokyo',
                            latitude=35.65910807942215,
                            longitude=139.70372892916203
                        )
                    elif event.message.text=='sticker' :
                        reply= StickerSendMessage(
                            package_id='1',
                            sticker_id='1'
                        )
                    elif event.message.text=='imagemap' :
                        reply= ImagemapSendMessage(
                            base_url='https://example.com/base',
                            alt_text='this is an imagemap',
                            base_size=BaseSize(height=1040, width=1040),
                            actions=[
                                URIImagemapAction(
                                    link_uri='https://example.com/',
                                    area=ImagemapArea(
                                        x=0, y=0, width=520, height=1040
                                    )
                                ),
                                MessageImagemapAction(
                                    text='hello',
                                    area=ImagemapArea(
                                        x=520, y=0, width=520, height=1040
                                    )
                                )
                            ]
                        )
                    elif event.message.text=='ButtonsTemplate' :
                        reply= TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                thumbnail_image_url='https://example.com/image.jpg',
                                title='Menu',
                                text='Please select',
                                actions=[
                                    PostbackTemplateAction(
                                        label='postback',
                                        text='postback text',
                                        data='action=buy&itemid=1'
                                    ),
                                    MessageTemplateAction(
                                        label='message',
                                        text='message text'
                                    ),
                                    URITemplateAction(
                                        label='uri',
                                        uri='http://example.com/'
                                    )
                                ]
                            )
                        )
                    elif event.message.text=='ConfirmTemplate' :
                        reply= TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                thumbnail_image_url='https://example.com/image.jpg',
                                title='Menu',
                                text='Please select',
                                actions=[
                                    PostbackTemplateAction(
                                        label='postback',
                                        text='postback text',
                                        data='action=buy&itemid=1'
                                    ),
                                    MessageTemplateAction(
                                        label='message',
                                        text='message text'
                                    ),
                                    URITemplateAction(
                                        label='uri',
                                        uri='http://example.com/'
                                    )
                                ]
                            )
                        )
                    elif event.message.text=='ConfirmTemplate' :
                        reply= TemplateSendMessage(
                                alt_text='Confirm template',
                                template=ConfirmTemplate(
                                    text='Are you sure?',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='postback',
                                            text='postback text',
                                            data='action=buy&itemid=1'
                                        ),
                                        MessageTemplateAction(
                                            label='message',
                                            text='message text'
                                        )
                                    ]
                                )
                            )
                    elif event.message.text=='CarouselTemplate' :
                        reply=TemplateSendMessage(
                            alt_text='Carousel template',
                            template=CarouselTemplate(
                                columns=[
                                    CarouselColumn(
                                        thumbnail_image_url='https://example.com/item1.jpg',
                                        title='this is menu1',
                                        text='description1',
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback1',
                                                text='postback text1',
                                                data='action=buy&itemid=1'
                                            ),
                                            MessageTemplateAction(
                                                label='message1',
                                                text='message text1'
                                            ),
                                            URITemplateAction(
                                                label='uri1',
                                                uri='http://example.com/1'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url='https://example.com/item2.jpg',
                                        title='this is menu2',
                                        text='description2',
                                        actions=[
                                            PostbackTemplateAction(
                                                label='postback2',
                                                text='postback text2',
                                                data='action=buy&itemid=2'
                                            ),
                                            MessageTemplateAction(
                                                label='message2',
                                                text='message text2'
                                            ),
                                            URITemplateAction(
                                                label='uri2',
                                                uri='http://example.com/2'
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    elif event.message.text=='help' :
                        reply=TextSendMessage(text="text\nCarouselTemplate")
                    else:
                        reply=TextSendMessage(text=event.message.text)

                    line_bot_api.reply_message(
                        event.reply_token,
                        reply
                        # TextSendMessage(text=event.message.text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

        # {
        #     "type": "text",
        #     "text": "Hello, world"
        # }
        # 
        # {
        #   "type": "template",
        #   "altText": "this is a buttons template",
        #   "template": {
        #       "type": "buttons",
        #       "thumbnailImageUrl": "https://example.com/bot/images/image.jpg",
        #       "title": "Menu",
        #       "text": "Please select",
        #       "actions": [
        #           {
        #             "type": "postback",
        #             "label": "Buy",
        #             "data": "action=buy&itemid=123"
        #           },
        #           {
        #             "type": "postback",
        #             "label": "Add to cart",
        #             "data": "action=add&itemid=123"
        #           },
        #           {
        #             "type": "uri",
        #             "label": "View detail",
        #             "uri": "http://example.com/page/123"
        #           }
        #       ]
        #   }
        # }
        # 
        # 
        # {
        #   "type": "template",
        #   "altText": "this is a confirm template",
        #   "template": {
        #       "type": "confirm",
        #       "text": "Are you sure?",
        #       "actions": [
        #           {
        #             "type": "message",
        #             "label": "Yes",
        #             "text": "yes"
        #           },
        #           {
        #             "type": "message",
        #             "label": "No",
        #             "text": "no"
        #           }
        #       ]
        #   }
        # }
        # 
        # {
        #   "type": "template",
        #   "altText": "this is a carousel template",
        #   "template": {
        #       "type": "carousel",
        #       "columns": [
        #           {
        #             "thumbnailImageUrl": "https://example.com/bot/images/item1.jpg",
        #             "title": "this is menu",
        #             "text": "description",
        #             "actions": [
        #                 {
        #                     "type": "postback",
        #                     "label": "Buy",
        #                     "data": "action=buy&itemid=111"
        #                 },
        #                 {
        #                     "type": "postback",
        #                     "label": "Add to cart",
        #                     "data": "action=add&itemid=111"
        #                 },
        #                 {
        #                     "type": "uri",
        #                     "label": "View detail",
        #                     "uri": "http://example.com/page/111"
        #                 }
        #             ]
        #           },
        #           {
        #             "thumbnailImageUrl": "https://example.com/bot/images/item2.jpg",
        #             "title": "this is menu",
        #             "text": "description",
        #             "actions": [
        #                 {
        #                     "type": "postback",
        #                     "label": "Buy",
        #                     "data": "action=buy&itemid=222"
        #                 },
        #                 {
        #                     "type": "postback",
        #                     "label": "Add to cart",
        #                     "data": "action=add&itemid=222"
        #                 },
        #                 {
        #                     "type": "uri",
        #                     "label": "View detail",
        #                     "uri": "http://example.com/page/222"
        #                 }
        #             ]
        #           }
        #       ]
        #   }
        # }