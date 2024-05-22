from flask import Flask, flash, render_template, redirect, url_for, request, session


class IndexController:

    def index(self, db):
        return db.read(None)
