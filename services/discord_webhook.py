import asyncio
import aiohttp
import datetime

class DiscordWebhook:

    async def post_message(self, webhook_url, params):
        """Function to send a message to Discord using a webhook"""
        try:
            session = aiohttp.ClientSession()
            await session.post(webhook_url, json=params)
            await session.close()
        except aiohttp.client_exceptions.ClientConnectorError: #If internet down, don't crash
            await session.close()

    def create_embed(self, **kwargs):
        """Function to create embed object with passed args"""
        embed = {}
        embed["title"] = kwargs.get("title", None)
        embed["description"] = kwargs.get("description", None)
        embed["url"] = kwargs.get("url", None)
        embed["timestamp"] = kwargs.get("timestamp", None)
        embed["color"] = kwargs.get("color", None)
        embed["footer"] = kwargs.get("footer", None)
        embed["image"] = kwargs.get("image", None)
        embed["thumbnail"] = kwargs.get("thumbnail", None)
        embed["embed"] = kwargs.get("embed", None)
        embed["provider"] = kwargs.get("provider", None)
        embed["author"] = kwargs.get("author", None)
        embed["fields"] = kwargs.get("fields", None)
        for k in list(embed.keys()):
            if embed[k] == None:
                del embed[k]
        return(embed)

    def create_thumbnail_object(self, **kwargs):
        """Function to create thumbnail object for embed"""
        thumbnail = {}
        thumbnail["url"] = kwargs.get("url", None)
        thumbnail["proxy_url"] = kwargs.get("proxy_url", None)
        thumbnail["height"] = kwargs.get("height", None)
        thumbnail["width"] = kwargs.get("width", None)
        for k in list(thumbnail.keys()):
            if thumbnail[k] == None:
                del thumbnail[k]
        return(thumbnail)

    def create_video_object(self, **kwargs):
        """Function to create video object for embed"""
        video = {}
        video["url"] = kwargs.get("url", None)
        video["height"] = kwargs.get("height", None)
        video["width"] = kwargs.get("width", None)
        for k in list(video.keys()):
            if video[k] == None:
                del video[k]
        return(video)

    def create_image_object(self, **kwargs):
        """Function to create image object for embed"""
        image = {}
        image["url"] = kwargs.get("url", None)
        image["proxy_url"] = kwargs.get("proxy_url", None)
        image["height"] = kwargs.get("height", None)
        image["width"] = kwargs.get("width", None)
        for k in list(image.keys()):
            if image[k] == None:
                del image[k]
        return(image)

    def create_author_object(self, **kwargs):
        """Function to create author object for embed"""
        author = {}
        author["name"] = kwargs.get("name", None)
        author["url"] = kwargs.get("url", None)
        author["icon_url"] = kwargs.get("icon_url", None)
        author["proxy_icon_url"] = kwargs.get("proxy_icon_url", None)
        for k in list(author.keys()):
            if author[k] == None:
                del author[k]
        return(author)

    def create_footer_object(self, **kwargs):
        """Function to create footer object for embed"""
        footer = {}
        footer["text"] = kwargs.get("text", None)
        footer["icon_url"] = kwargs.get("icon_url", None)
        footer["proxy_icon_url"] = kwargs.get("proxy_icon_url", None)
        for k in list(footer.keys()):
            if footer[k] == None:
                del footer[k]
        return(footer)

    def create_field_object(self, **kwargs):
        """Function to create field object for embed"""
        field = {}
        field["name"] = kwargs.get("name", None)
        field["value"] = kwargs.get("value", None)
        field["inline"] = kwargs.get("inline", None)
        for k in list(field.keys()):
            if field[k] == None:
                del field[k]
        return(field)